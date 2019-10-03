#!/home/vince/Desktop/project/local/conda_env/str_prj/bin/python

from Tools import Gor,Dataset
import argparse
import pickle

# Global variables: path to test set folder
te_set = '/home/vince/Desktop/project/dataset/test/'

# Prediction procedure for GOR model. Considers the presence
# or not of a pre-existent Dataset() object. A trained model is mandatory. 
# This prediction is aimed to obtain a new Dataset() object on which 
# measure the performance of the predictor.
def testing(w,model,inlist=False,dat=False):
    if inlist:
        data = Dataset(w=w,path=te_set).getall(inlist)
        return Gor(w=w).predict(model,data)
    else:
        data = Dataset().load(dat)
        return Gor(w=w).predict(model,data)

# Define the type of operation to perform given the type of
# option choosen by the user.
def Main():
    parser = argparse.ArgumentParser(description='GOR testing procedure. v1.0')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-l',dest='inlist',type=str,\
        help='list of PDB IDs to build a test dataset')
    group.add_argument('-d',dest='dataset',type=str,\
        help='dataset object to be loaded for the prediction')
    parser.add_argument('-w',dest='window',type=int,default=17,\
        help='size of the sliding window. Default 17')
    parser.add_argument('-m',dest='model',type=str,required=True,\
        help='trained GOR model necessary to compute the prediction.')
    parser.add_argument('-o','--out',dest='output',type=str,required=True,\
        help='specify an ouput file to save the dataset containing the predictions.')

    args = parser.parse_args()
    
    model = Gor().load(args.model); w = args.window; output = args.output
    if args.inlist:
        inlist = args.inlist
        prediction = testing(w,model,inlist=inlist)
    elif args.dataset:
        dat = args.dataset
        prediction = testing(w,model,dat=dat)
    
    # Save the Dataset() object in an output file.
    with open(output+'.test','wb') as outfile:
        pickle.dump(prediction,outfile,protocol=pickle.HIGHEST_PROTOCOL)
    
    return 'The prediction has been performed successfully. Ouput was saved at %r'%(output+'.test')

if __name__=='__main__':
    Main()