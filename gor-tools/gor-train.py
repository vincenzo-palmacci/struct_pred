#!/home/vince/Desktop/project/local/conda_env/str_prj/bin/python

from Dataset import *
from Gor import Gor
import sys
import argparse

# Global variables: path to training set folder
tr_set = '/home/vince/Desktop/project/dataset/training/' 


# Training procedure for GOR model. Considers the presence
# or not of a pre-existent Dataset() object.
def training(w,inlist=False,dat=False):
    if inlist:
        pssm = Profile().get_dict(tr_set,inlist,'psiblast')
        dssp = Sequence().get_dict(tr_set,inlist,'dssp')
        data = Dataset.build('training',pssm,dssp)
        return Gor(w=w).train(data)
    else:
        data = Dataset.load(dat)
        return Gor(w=w).train(data)

# Define the type of operation to perform given the type of
# option choosen by the user.
def Main():
    parser = argparse.ArgumentParser(description='Vincenzo 14/10/2019: GOR training procedure. v1.1')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-l',dest='inlist',type=str,\
        help='list of PDB IDs to build a training dataset')
    group.add_argument('-d',dest='dataset',type=str,\
        help='dataset object to be loaded for the training')
    parser.add_argument('-w',dest='window',type=int,default=17,\
        help='size of the sliding window. Default 17')
    parser.add_argument('-o','--out',dest='out',type=str,\
        help='specify an ouput file. Default stdout')

    args = parser.parse_args()
    
    w = args.window
    if args.inlist:
        inlist = args.inlist
        trained = training(w,inlist=inlist)
    elif args.dataset:
        dat = args.dataset
        trained = training(w,dat=dat)

    if args.out: 
        trained.dump(args.out+'.model')
        return print('Trained model successfully saved at %r'%(args.out+'.model'))
    else:
        return print(trained)

if __name__=='__main__':
    Main()