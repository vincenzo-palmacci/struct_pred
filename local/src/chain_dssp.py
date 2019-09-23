#!/home/vince/anaconda2/envs/lab2/bin/python

'''
Take a dssp file obtained from a PDB and perform the following operations:
consider only the data associated to a specific chain;
print a sse sequence according to the 3 element classifications.
'''

import sys 

# modify the string to obtain a 3 element classification
def replace_multiple(sequence):
    H = ['H','G','I']
    E = ['B','E']
    C = ['S','T',' ']
    
    # change the secondary structure assignment according to the 3 element classification
    seq = ''
    for ch in sequence:
        if ch in C: seq += '-'
        elif ch in E: seq += 'E'
        else: seq += 'H'
    
    # return the correct sequence of sse
    return  seq

# get a specific chain from a dssp file
def chain_dssp(indssp,pdbid,chain):
    flag = 0 # initialize a flag
    seq = '' # initialize an empty sequence

    for line in indssp:
        if line.find('  #  RESIDUE') == 0:
            flag = 1
            continue
        if flag == 1:
            if line[11] == chain: # postion of the chain in the dssp file
                seq += (line[16]) # add the corresponding ss assignment

    seq = replace_multiple(seq) # transform the original sequence mapping 8 sse to 3 sse
    return seq

if __name__ == '__main__':
    try:
        sys.argv[1] # list of representative ids : PDB_CHAIN
    except:
        print ('Usage: script.py <representative>.txt')
        raise SystemExit
    else:
        with open(sys.argv[1]) as inlist:
            # iterate over a list of representative id_chain
            for line in inlist:
                pdb_id = line.rstrip().split('_')[0] #  pdb id 
                chain_id = line.rstrip().split('_')[1] # chain identifier 
                header = ('>'+ pdb_id +'_'+chain_id) # store the correct header
                
                try:
                    open(pdb_id+'.pdb.dssp')
                except:
                    pass
                else:
                    # open the .dssp file corresponding to the pdb id
                    with open(pdb_id+'.pdb.dssp') as indssp, open(pdb_id+'_'+chain_id+'.dssp','w') as outfile:
                        outfile.write(header+'\n')
                        outfile.write(chain_dssp(indssp,pdb_id,chain_id)+'\n')