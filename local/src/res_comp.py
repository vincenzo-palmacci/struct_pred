#!/home/vince/anaconda2/envs/lab2/bin/python

'''
Plot the composition in secondary structure for each residue.
Working directory: pre_statistics
'''

import pandas as pd
import matplotlib.pyplot as plt
import sys 

# initialize a dictionariy of dictionaries : D = {sse:{res:val}} 
def initialize_dic():
    res = ["A", "R", "N", "D", "C", "E", "Q", "G", "H", "I", # list of residues
           "L", "K","M", "F", "P", "S", "T", "W", "Y", "V",]
    sse = ['H','E','C','O'] # choose the sse to consider. O is for the Overall
    d = {} # empty dictionary
    for element in sse:
        for ch in res:
            d[element] = d.get(element, dict())
            d[element][ch] = d[element].get(ch, 0)

    return d

def normalized_df(s):
    sse = ['H','E','C','O']
    df = pd.DataFrame(s)
    total = sum(list(df['O']))
    
    return df.divide(total) 

# count how many times a specific sse is assigned to each residue 
def Main(infasta, indssp, d):
    # initialize a dictionary for each ss considered + one for computing the overall 
    for line in zip(indssp, infasta):
        struc = line[0].rstrip()
        seq = line[1].rstrip()
        for ss, ch in zip(struc, seq):
            if ss == '-':
                ss = 'C'
            # start counting all the residues
            d['O'][ch] = d['O'].get(ch, 0)
            d['O'][ch] += 1
            # count the residues associated to a specific secondary structure
            d[ss][ch] = d[ss].get(ch, 0)
            d[ss][ch] += 1 

    return d

if __name__ == '__main__':
    try:
        MULTI_DSSP = sys.argv[1] # file containing the listed dssp assignments
        MULTI_FASTA = sys.argv[2] # file containing the listed fasta sequences
    except:
        print ('Usage: script.py <listedfile>.dssp <listedfile>.fasta')
        raise SystemExit
    else:
        with open(sys.argv[1]) as indssp, open(sys.argv[2]) as infasta:
            D = initialize_dic() # return an initialized empy dictionary of dictionaries D = {sse:{res:val}}
            S = (Main(infasta, indssp, D)) # return the dictionaries with all the counters updated
            DF = normalized_df(S) # transform the dictionary into a DataFrame. All the values are normalized
        
        print (DF)
        
        # plot the histogram computed from the DataFrame
        DF.plot.bar(rot = 0)
        plt.show()