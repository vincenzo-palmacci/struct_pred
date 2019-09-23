#!/home/vince/anaconda2/envs/lab2/bin/python

'''
Parse blastclust output.
Working directory: blind_set
'''

import pandas as pd 
import sys

# parse a csv table and output a df frame with specific features
def parse_csv(intable):
    df = pd.read_csv(intable)
    df['ENTITY'] = df['PDB ID'] + '_' + df['Chain ID']

    df = df[['ENTITY','Resolution']]

    return df

# associate to each pdbid the resolution and print the representative for each cluster
def parse_cluster(incluster, df):
    best = [] # initialize a list to save the representatives

    for line in incluster:
        # two variables to save the temporary best
        best_pdbid = ''
        best_res = float()
        line = line.rstrip().split() # list of id for each cluster
        
        # find the representative comparing the elements iteratively
        for ide in line:
            pdbid = ide
            res = float(df[df['ENTITY'] == ide]['Resolution'])
            if res > best_res:
                best_pdbid = pdbid
                best_res = res
        # append the best to the list
        best.append([best_pdbid,best_res])
    return best

if __name__ == '__main__':
    try:
        PDB_TABLE = sys.argv[1] # df from the csv
        CLUSTER = sys.argv[2] # file containing the output of blastclust
    except:
        print ('Usage: script.py <pdb>.csv <blastclust>.clust')
        raise SystemExit
    else:
        DF = parse_csv(sys.argv[1])
        with open(sys.argv[2]) as incluster: # file containing the output of blastclust
            # print the formatted representative 
            for val in parse_cluster(incluster, DF): 
                print (val[0]) # print the PDB_ID of the representative of each cluster