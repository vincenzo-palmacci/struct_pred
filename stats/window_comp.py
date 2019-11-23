#!/home/vince/Desktop/project/local/conda_env/str_prj/bin/python

'''
Statistics accounting for the context of the residues.
The operation is performed using the sliding windows method.
'''

from Dataset import Dataset
import argparse
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def init_dict(w):
    window = dict((i,{})for i in range(w))
    res = ["G","A","V","P","L","I","M","F","W","Y",
           "S","T","C","N","Q","H","D","E","K","R"]
    for key in window:
        for index in res:
            window[key][index] = window[key].get(index,0)
    return window

# Pad dssp and pssm according to the window's size.
def padding(w,obj):
    if type(obj) == str:
        pad = '-'*(w//2)
        obj = pad+obj+pad
    return obj

def window_comp(dataset,w,sse):    
    i, j, k = 0, w//2, w
    window = init_dict(w) 
    for key in dataset:
        dssp = padding(w,dataset[key]['dssp'])
        fasta = padding(w,dataset[key]['fasta'])
        while k <= len(dssp):
            if dssp[j] == sse:
                for index in range(i,k):
                    if fasta[index] not in window[index-i]:
                        pass
                    else:
                        window[index-i][fasta[index]] +=1
            i, j, k = i+1, j+1, k+1
        i, j, k = 0, w//2, w
    return pd.DataFrame(window)

def Main():
    parser = argparse.ArgumentParser(description='Dataset computing procedure. v1.0')
    parser.add_argument('-d',dest='dataset',type=str,required=True,\
        help='input dataset')
    parser.add_argument('-w',dest='window',type=int,default=17,\
        help='window sizw')

    args = parser.parse_args()

    dataset = Dataset.load(args.dataset) ; w = args.window

    for sse in ['H','E','-']:
        df = window_comp(dataset,w,sse)
        df.columns = ['-8','-7','-6','5','-4','-3','-2','-1','0','1','2','3','4','5','6','7','8']
        fig, ax = plt.subplots()
        heatmap = ax.pcolor(df,cmap="Blues")
        cbar = plt.colorbar(heatmap)
        ax.set_xticks(np.arange(df.shape[1]) + 0.5, minor=False)
        ax.set_yticks(np.arange(df.shape[0]) + 0.5, minor=False)
        ax.set_xticklabels(df.columns)
        ax.set_yticklabels(df.index)

        plt.show()

if __name__ == '__main__':
    Main()