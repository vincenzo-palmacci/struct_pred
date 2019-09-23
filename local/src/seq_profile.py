#!/home/vince/anaconda2/envs/lab2/bin/python

'''
Compute the sequence profile using the output PSSM of PSIBLAST.
The file <filename>.pssm is cleaned and only the conter is retained.
Working directory: profile_gen
'''

import sys
import numpy as np

def compute_profile(inpssm):
    matrix = [] # initialize an empty list

    # for each line in the input compute a list of values
    for line in inpssm:
        pssm = line.rstrip().split()[22:-2]
        # for each element in the list transform that element in a int
        for ch in range(len(pssm)):
            pssm[ch] = int(pssm[ch])
        matrix.append(pssm) # append each list to the "matrix"

    array = np.array(matrix) # transform the matrix in a numpy.array

    array = np.true_divide(array, 100) # transform the values

    return array
        
if __name__=='__main__':
    try:
        sys.argv[1] # input: grep -E "^[[:space:]]*[0-9]" <filename>.pssm
        sys.argv[2]
    except:
        print ('Usage: script.py <clean_matrix>.pssm')
        raise SystemExit
    else:    
        with open(sys.argv[1]) as inpssm:  
            np.save(sys.argv[2]+'.npy', compute_profile(inpssm))