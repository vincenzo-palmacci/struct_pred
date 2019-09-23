#!/home/vince/anaconda2/envs/lab2/bin/python

'''
Training procedure of the GOR method implementation.
Takes in input a list of ids, then open the fasta sequence,
the dssp sequence and load the profile associated to each 
id.
'''

import sys
import numpy as np

def training(inlist,sse):

    m = np.zeros([17,20]) # initialize an empty matrix
    counter = 0 # one counter for the total
    ss_counter = 0

    for val in inlist:
        # initialize 3 counters for the sliding window
        i, j, k = 0, 0, 8
        
        domain_id = val.rstrip() # save the domain identifier

        # check if the profile exists for the given id the input list
        try: 
            np.load('npy/'+domain_id+'.pssm.npy')
        except:
            pass
        else:
            inpssm = np.load('npy/'+domain_id+'.pssm.npy') # load the profile
            
            # open the files from different folders 
            with open('fasta/'+domain_id+'.fasta') as infasta, open('dssp/'+domain_id+'.dssp') as indssp:

                # iterate over the files, and consider only the sequence
                for line in zip(infasta,indssp):
                    if '>' not in line[0]:
                        seq = line[0].rstrip() 
                        struc = line[1].rstrip()
                        counter += len(seq)
                        
                        # consider from residue 0 to 8 as the central residue in the window
                        while j <= 8:
                            if struc[j] == sse:
                                ss_counter += 1
                                m[8-j:] += inpssm[:k+1] 
                            k, j = k+1, j+1
                        
                        while k < len(seq):
                            if struc[j] == sse:
                                ss_counter += 1 
                                m += inpssm[i:k]
                            i, j, k = i+1, j+1, k+1

                        # consider the last 8 residues as central in the window
                        while j < k:
                            if struc[j] == sse:
                                ss_counter += 1 
                                m[:k-i] += inpssm[i:]
                            i, j = i+1, j+1

                i, j, k = 0, 8, 17
    
    norm = np.array(m)/int(counter)
    ss_freq = ss_counter/counter
    return norm, ss_freq

if __name__ == '__main__':
    try:
        sys.argv[1]
    except:
        print('Usage <pdb_id>.list')
    else:
        for sse in ['H','E','-']: # repeat the process for each sse you want to consider
            with open(sys.argv[1]) as inlist:
                # save the results as numpy object
                if sse == 'H': H, H_freq = training(inlist,sse)
                elif sse == 'E': S, S_freq = training(inlist,sse)
                else: C, C_freq = training(inlist,sse)
        
        Overall = H + S + C
        
        # save the matrices containing the information for each residue tipe at each position in the window
        np.save('infoH',np.log2(H/(Overall*H_freq))); np.save('infoE',np.log2(S/(Overall*S_freq))); np.save('infoC',np.log2(C/(Overall*C_freq)))