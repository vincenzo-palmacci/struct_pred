#!/home/vince/Desktop/project/local/conda_env/str_prj/bin/python

from Dataset import *
import sys
import argparse

'''
Make a Dataset.
'''

# Global variables: path to test set folder
prj = '/home/vince/Desktop/project/dataset/'

def make_dataset(path,inlist,mode):
    pssm = Profile().get_dict(path,inlist,'psiblast')
    dssp = Sequence().get_dict(path,inlist,'dssp')
    #if mode == 'training':
    fasta = Sequence().get_dict(path,inlist,'fasta')
    return Dataset.build(mode,pssm,dssp,fasta)
    #else:
    #    return Dataset.build(mode,pssm,dssp)

def Main():
    parser = argparse.ArgumentParser(description='Dataset computing procedure. v1.0')
    parser.add_argument('-l',dest='inlist',type=str,required=True,\
        help='list of PDB IDs to build a test dataset')
    parser.add_argument('-m','--mode',dest='mode',type=str,required=True,\
        help='define training or test')
    parser.add_argument('-o','--out',dest='out',type=str,required=True,\
        help='specify an ouput file.')

    args = parser.parse_args()
    path = prj+args.mode+'/'; inlist = args.inlist

    data = make_dataset(path,inlist,args.mode)
    data.dump(args.out+'.dat')
    return print('Dataset succesfully saved at %r'%(args.out+'.dat'))

if __name__=='__main__':
    Main()