#!/home/vince/anaconda2/envs/lab2/bin/python

'''
Compare the lenght of the dssp assignment and the fasta sequence
of the same pdb entry.
'''
import sys

# initialize a dictionary containing all the ids
def initialize_dict(inlist):
    d = {}
    for line in inlist:
        d[line.rstrip()] = d.get(line.rstrip(),['',''])

    return d

# fill the dictionary associating to each identifier(key) teo values: the fasta sequence and the dssp assignment
def fill_dict(infasta,indssp,d):

    for seq in infasta:
        if '>' in seq:
            d[seq.rstrip().split('>')[1]][0] = next(infasta,'').rstrip()

    for struc in indssp:
        if '>' in struc:
            d[struc.rstrip().split('>')[1]][1] = next(indssp,'').rstrip()
    
    return d

# compare the lenght of the values and return a list of filtered ids
def compare_len(d):
    equal = []
    for key in d:
        if len(d[key][0]) == len(d[key][1]): # consider only the keys for which the two values are of the same lenght
            equal.append(key)

    return equal
    
if __name__ == '__main__':
    try:
        sys.argv[1]
        sys.argv[2]
        sys.argv[3]
    except:
        print ('Usage: script.py <representative>.list <concatenated>.fasta <cancatenated>.dssp')
    else:
        with open(sys.argv[1]) as inlist: # open the list of ids
            D = initialize_dict(inlist)
        with open(sys.argv[2]) as infasta, open(sys.argv[3]) as indssp: # open the files containing the concatenated fasta sequences and dssp assignments
            S = fill_dict(infasta,indssp,D)
            
            # just to print a ordered list of ids 
            for val in compare_len(S):
                print (val)
            
            '''
            for line in (fill_dict(infasta,indssp,D)):
                for val in (D[line]):
                    print (line)
                    print (val)
            '''