#!/home/vince/Desktop/project/local/conda_env/str_prj/bin/python

from Dataset import Dataset
import sys
import numpy as np
import argparse

classes = {'H':1,'E':2,'-':3}

# Pad dssp and pssm according to the window's size.
def padding(w,obj):
    if type(obj) == str:
        pad = '-'*(w//2)
        obj = pad+obj+pad
    else:
        pad = np.zeros((w//2,20))
        obj = np.vstack((pad,obj,pad))
    return obj

# Produce a string in which each row is a vector containing the class in
# first position and then a vector containing the profile info (enumerated)
# for the profile corresponding to a window of size w.
def encode(w,data):
    tot = ''
    for key in data:
        dssp = padding(w,data[key]['dssp'])
        pssm = padding(w,data[key]['pssm'])
        encoded = ''
        i, j, k = 0, w//2, w
        while k <= len(pssm):
            h = 1; tmp_str = ''
            for line in pssm[i:k]:
                for val in line:
                    if val:
                        tmp_str += ' %s:%s '%(h,val)
                    h += 1
            encoded += '%s %s\n'%(classes[dssp[j]],tmp_str)
            i, j, k = i+1, j+1, k+1
        tot += encoded
    return tot

# Define the type of operation to perform given the type of
# option choosen by the user.
def Main():
    parser = argparse.ArgumentParser(description='Vincenzo 11/11/2019: SVM input encoding. v1.1')
    parser.add_argument('-d',dest='dataset',type=str,required=True,\
        help='dataset object to be loaded for the encoding')
    parser.add_argument('-w',dest='window',type=int,default=17,\
        help='size of the sliding window. Default 17')
    parser.add_argument('-o','--out',dest='out',type=str,required=True,\
        help='specify an ouput file. Default stdout')

    args = parser.parse_args()

    w = args.window ; data = Dataset.load(args.dataset)
    
    encoded_string = encode(w,data) 

    with open(args.out+'.input.dat', 'w') as outfile:
        outfile.write(encoded_string)


    return print('Input encoded successfully and saved at %r'%(args.out+'input.dat'))

if __name__=='__main__':
    Main()