#!/home/vince/Desktop/project/local/conda_env/str_prj/bin/python

#!/home/vince/Desktop/project/local/conda_env/str_prj/bin/python

from Tools import Gor,Dataset
import argparse

# Global variables: path to training set folder
tr_set = '/home/vince/Desktop/project/dataset/training/' 


# Training procedure for GOR model. Considers the presence
# or not of a pre-existent Dataset() object.
def training(w,inlist=False,dat=False):
    if inlist:
        data = Dataset(w=w,path=tr_set).getall(inlist)
        return Gor(w=w).train(data)
    else:
        data = Dataset().load(dat)
        return Gor(w=w).train(data)

# Define the type of operation to perform given the type of
# option choosen by the user.
def Main():
    parser = argparse.ArgumentParser(description='GOR training procedure. v1.0')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-l',dest='inlist',type=str,\
        help='list of PDB IDs to build a training dataset')
    group.add_argument('-d',dest='dataset',type=str,\
        help='dataset object to be loaded for the training')
    parser.add_argument('-w',dest='window',type=int,default=17,\
        help='size of the sliding window. Default 17')
    parser.add_argument('-o','--out',dest='output',type=str,\
        help='specify an ouput file to save the trained model. Default stdout')

    args = parser.parse_args()
    
    w = args.window
    if args.inlist:
        inlist = args.inlist
        trained = training(w,inlist=inlist)
    elif args.dataset:
        dat = args.dataset
        trained = training(w,dat=dat)

    if args.output: 
        trained.dump(output+'.model')
        return 'Trained model succesfully saved at %r'%(output+'.model')
    else:
        return print(trained)

if __name__=='__main__':
    Main()