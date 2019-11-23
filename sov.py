#!/home/vince/Desktop/project/local/conda_env/str_prj/bin/python

from Dataset import Dataset
import numpy as np
import argparse

def set_parser(dataset,key,obj,sse):
    seq = dataset[key][obj]
    index = 0 ; seq_set = []
    while index < len(seq):
        tmp_list = []
        while seq[index] == sse and index < (len(seq)-1):
            tmp_list.append(index)
            index +=1
        seq_set.append(set(tmp_list))
        index += 1
    return seq_set

def sov_per_structure(dataset,genre,sse,step=False):
    per_seq_sov = []
    for key in dataset:
        obs = set_parser(dataset,key,'dssp',sse)
        pred = set_parser(dataset,key,str(genre),sse)
        tmp_list = [] ; normalizer = 0
        for s in obs:
            flag = 1
            for t in pred:
                if s&t:
                    flag = 0
                    normalizer += len(s)
                    minov = len(s&t)
                    maxov = len(s|t)
                    delta = min([minov,maxov-minov,len(s)//2,len(t)//2])
                    tmp_list.append(((minov+delta)/maxov)*len(s))
            if flag == 1:
                normalizer += len(s)
        if normalizer:
            tmp_list = sum(tmp_list)*100*(1/normalizer)
            per_seq_sov.append(tmp_list)
    return sum(per_seq_sov)/len(per_seq_sov)

def sov_multi(dataset,genre):
    pass

# Define the type of operation to perform given the type of
# option choosen by the user.
def Main():
    parser = argparse.ArgumentParser(description='Vincenzo 12/11/2019: SOV computation. v1.1')
    parser.add_argument('-d',dest='dataset',type=str,required=True,\
        help='dataset object to be loaded for the training')
    parser.add_argument('-t','--type',dest='genre',type=str,required=True,\
        help='specify the type of prediction to be tested: SVM or GOR')

    args = parser.parse_args()

    sse_list = ['H','E','-'] ; dataset = Dataset.load(args.dataset) ; genre = args.genre

    for sse in sse_list:
        print ('%s : %s'%(sse,sov_per_structure(dataset,genre,sse)))

if __name__ == '__main__':
    Main()
    print ('TO BE COMPLETED: Multiclass SOV')