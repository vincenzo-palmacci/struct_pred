#!/home/vince/anaconda2/envs/lab2/bin/python

import sys
import numpy as np


def predict(inpssm):
    H = np.load('infoH.npy'); E =np.load('infoE.npy'); C =np.load('infoC.npy')

    i, k = 0, 9

    seq = ''

    # consider from residue 0 to 8 as the central residue in the window
    while k < 17:
        probs = []
        probH = np.sum(H[17-k:]*inpssm[i:k]); probE = np.sum(E[17-k:]*inpssm[i:k]); probC = np.sum(C[17-k:]*inpssm[i:k])
        probs.append(probH); probs.append(probE); probs.append(probC)
        if max(probs) == probH: seq += 'H'
        elif max(probs) == probE: seq += 'E'
        else: seq += '-' 
        k = k+1

    while k < len(inpssm):
        probs = []
        probH = np.sum(H*inpssm[i:k]); probE = np.sum(E*inpssm[i:k]); probC = np.sum(C*inpssm[i:k])
        probs.append(probH); probs.append(probE); probs.append(probC)
        if max(probs) == probH: seq += 'H'
        elif max(probs) == probE: seq += 'E'
        else: seq += '-'
        i, k = i+1, k+1
    
    # consider the last 8 residues as central in the window
    while i < k-8:
        probs = []
        probH = np.sum(H[:k-i]*inpssm[i:k]); probE = np.sum(E[:k-i]*inpssm[i:k]); probC = np.sum(C[:k-i]*inpssm[i:k])
        probs.append(probH); probs.append(probE); probs.append(probC)
        if max(probs) == probH: seq += 'H'
        elif max(probs) == probE: seq += 'E'
        else: seq += '-'
        i += 1

    return seq

if __name__=='__main__':
    try:
        sys.argv[1]
    except:
        print('Usage: script.py <pdb_id>')
        raise SystemExit
    else:
        inpssm = np.load('npy/'+sys.argv[1]+'.pssm.npy')
        print('>'+sys.argv[1])
        print (predict(inpssm))