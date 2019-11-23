#!/home/vince/Desktop/project/local/conda_env/str_prj/bin/python

from Dataset import *
from Gor import Gor
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
        pssm = Profile().get_dict(te_set,inlist,'psiblast')
        dssp = Sequence().get_dict(te_set,inlist,'dssp')
        data = Dataset.build('test',dssp,pssm)
        Gor(w=w).predict(model,data)
        return data
    else:
        data = Dataset.load(dat)
        Gor(w=w).predict(model,data)
        return data

# Define the type of operation to perform given the type of
# option choosen by the user.
def Main():
    parser = argparse.ArgumentParser(description='Vincenzo 14/10/2019: GOR testing procedure. v1.1')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-l',dest='inlist',type=str,\
        help='list of PDB IDs to build a test dataset')
    group.add_argument('-d',dest='dataset',type=str,\
        help='dataset object to be loaded for the prediction')
    parser.add_argument('-w',dest='window',type=int,default=17,\
        help='size of the sliding window. Default 17')
    parser.add_argument('-m',dest='model',type=str,required=True,\
        help='trained GOR model necessary to compute the prediction.')
    parser.add_argument('-o','--out',dest='out',type=str,required=True,\
        help='specify an ouput file.')

    args = parser.parse_args()
    
    model = Gor().load(args.model); w = args.window
    if args.inlist:
        inlist = args.inlist
        prediction = testing(w,model,inlist=inlist)
    elif args.dataset:
        dat = args.dataset
        prediction = testing(w,model,dat=dat)
    
    # Save the Dataset containing the predictions in an output file.
    prediction.dump(args.out+'.test')
    
    return print('The prediction has been performed successfully. Ouput was saved at %r'%(args.out+'.test'))

if __name__=='__main__':
    Main()