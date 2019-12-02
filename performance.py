#!/home/vince/Desktop/project/local/conda_env/str_prj/bin/python

from Dataset import Dataset
import numpy as np
from sklearn.metrics import multilabel_confusion_matrix as mcm
import pandas as pd
import argparse
from sov import sov_per_structure, set_parser, sov_multi
from math import sqrt

'''
Compute the performances of multiclass classification methods. A multilabel
confusion matrix is employed and different quality indexes are defined.
'''

# Compute the Accuracy: (TP+TN)/N
def acc(m):
    return ((m[0,0]+m[1,1])/np.sum(m))*100

# Compute Matthew's correlation coefficent:
# (TP*TN+FP*FN)/sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
def mcc(m):
    numerator = m[0,0]*m[1,1]-m[1,0]*m[0,1]
    denominator = (m[1,1]+m[0,1])*(m[1,1]+m[1,0])*(m[0,0]+m[0,1])*(m[0,0]+m[1,0])
    return (numerator/np.sqrt(denominator))*100

# Compute thr Positive Predicted Value: TP/(TP+FP)
def ppv(m):
    return (m[1,1]/(m[1,1]+m[0,1]))*100

# Compute the Sensitivity(or Recall): TP/(TP+FN)
def sen(m):
    return (m[1,1]/(m[1,1]+m[1,0]))*100

# Compute a binary confusion matrix for each element of secondary
# structure. For ech matrix the statistics are computed.
def conf_matrix(dataset,genre):
    true_data =  []; pred_data = []
    for key in dataset:
        true_data.extend(dataset[key]['dssp']) # Extend the lists with all the predicted
        pred_data.extend(dataset[key][str(genre)]) # and observed secondary structure assignments.
    conf_matr = mcm(true_data,pred_data,labels=["H", "E", "-"])
    measures = {}; sse = ["H", "E", "-"]
    for val in range(3):
        measures[sse[val]] = measures.get(sse[val],[])
        measures[sse[val]].append(acc(conf_matr[val]))
        measures[sse[val]].append(mcc(conf_matr[val]))
        measures[sse[val]].append(sen(conf_matr[val]))
        measures[sse[val]].append(ppv(conf_matr[val]))
    sov_scores = sov_multi(dataset,genre)
    for val in range(3):
        measures[sse[val]].append(sov_scores[1][sse[val]])
    Q3 = np.sum([conf_matr[i][1,1]for i in range(3)])/np.sum(conf_matr[0])
    SOV_mean = sov_scores[0]    
    df = pd.DataFrame(measures,index=['ACC','MCC','SEN','PPV','SOV'])
    return df,Q3*100,SOV_mean # Return a DataFrame

def compute_deviation(mean,folds,Q3,SOV):
    std_dev_df, std_dev_Q3, std_dev_sov = [], [], []
    for val in range(5):
        std_dev_df.append((folds[val].sub(mean[0]))**2)
        std_dev_Q3.append((Q3[val]-mean[1])**2)
        std_dev_sov.append((SOV[val]-mean[2])**2)
    std_err_df = ((sum(std_dev_df)/4)**(1/2))/sqrt(5)
    std_err_Q3 = ((sum(std_dev_Q3)/4)**(1/2))/sqrt(5)
    std_err_sov = ((sum(std_dev_sov)/4)**(1/2))/sqrt(5)

    print ('%s\nQ3 : %s\n'%(std_err_df,std_err_Q3))
    return print('SOV : %s\n'%(std_err_sov))

# Define the type of operation to perform given the type of
# option choosen by the user.
def Main():
    parser = argparse.ArgumentParser(description='Vincenzo 12/11/2019: SOV computation. v1.1')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d',dest='dataset',type=str,\
        help='dataset object to be loaded for the training')
    group.add_argument('-f',dest='infile',type=str,\
        help='file containing the list of test set')
    parser.add_argument('-t','--type',dest='genre',type=str,required=True,\
        help='specify the type of prediction to be tested: SVM or GOR')

    args = parser.parse_args()

    genre = args.genre
    
    if args.infile:
        folds = [] ; scores = [] ; sovs = []
        with open(args.infile) as infile:
            for line in infile.readlines():
                line = line.rstrip()
                dataset = Dataset.load(line)
                folds.append(conf_matrix(dataset,genre)[0])
                scores.append(conf_matrix(dataset,genre)[1])
                sovs.append(conf_matrix(dataset,genre)[2])
                print('%s\nQ3 : %s'%(conf_matrix(dataset,genre)[0],conf_matrix(dataset,genre)[1]))
                print('SOV : %s\n'%(conf_matrix(dataset,genre)[2]))
        mean = sum(folds)/5,sum(scores)/5,sum(sovs)/5
        print ('%s\nQ3 : %s'%(mean[0],mean[1]))
        print ('SOV : %s\n'%(mean[2]))
        return compute_deviation(mean,folds,scores,sovs)

    else:
        dataset = Dataset.load(args.dataset)
        return print('%s\nQ3 : %s\nSOV : %s\n'%(conf_matrix(dataset,genre)[0],conf_matrix(dataset,genre)[1],conf_matrix(dataset,genre)[2]))



if __name__ == '__main__':
    Main()