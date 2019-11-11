#!/home/vince/Desktop/project/local/conda_env/str_prj/bin/python

from Dataset import *
from Gor import Gor
import pickle
import argparse

tr_set = '/home/vince/Desktop/project/dataset/training/'

def training(inlist):
	pssm = Profile().get_dict(tr_set,inlist,'psiblast')
	dssp = Sequence().get_dict(tr_set,inlist,'dssp')
	data = Dataset.build('train',dssp,pssm)
	return Gor().train(data)

def testing(model,inlist):
	pssm = Profile().get_dict(tr_set,inlist,'psiblast')
	dssp = Sequence().get_dict(tr_set,inlist,'dssp')
	data = Dataset.build('test',dssp,pssm)
	return data

def Main():
	parser = argparse.ArgumentParser(description='Vincenzo 14/10/2019: GOR cross-validation procedure. v1.1')
	parser.add_argument('--dir',dest='dir',type=str,required=True,\
		help='Directory containing training and testing lists')
	parser.add_argument('-c','--cycle',dest='num',type=int,required=True,\
	    help='specify number of folds.')
	parser.add_argument('-o','--out',dest='out',type=str,required=True,\
	    help='specify an ouput file.')
	
	args = parser.parse_args()
	folds = args.num
	for val in range(1,folds+1):
		folder = args.dir+str(val)
		model = training(folder+'/cv.train.id'); output = args.out+str(val)
		prediction = testing(model,folder+'/cv.test.id')
		
		prediction.dump(output+'.cv')

if __name__=='__main__':
	Main()