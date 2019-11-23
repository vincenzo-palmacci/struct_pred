#!/home/vince/Desktop/project/local/conda_env/str_prj/bin/python

'''
Plot the composition of the residues.
'''

from Dataset import Dataset
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from collections import OrderedDict
import matplotlib.ticker as mtick

def res_count(dataset):
    sse = {'H':OrderedDict(),'E':OrderedDict(),
           '-':OrderedDict(),'O':OrderedDict()}
    res = ["G","A","V","P","L","I","M","F","W","Y",
           "S","T","C","N","Q","H","D","E","K","R"]
    for key in sse:
        for index in res:
            sse[key][index] =sse[key].get(index,0)
    for key in dataset:
        for index in zip(dataset[key]['fasta'],dataset[key]['dssp']):
            if index[0] == 'X': pass
            else: 
                sse[index[1]][index[0]] += 1
                sse['O'][index[0]] += 1
    return pd.DataFrame(sse)

def Main():
    parser = argparse.ArgumentParser(description='Dataset computing procedure. v1.0')
    parser.add_argument('-d',dest='dataset',type=str,required=True,\
        help='input dataset')

    args = parser.parse_args()

    dataset = Dataset.load(args.dataset)

    df = res_count(dataset)/(sum(res_count(dataset)['O']))*100
    df.columns = ['Helix','Strand','Coil','Overall']
    df = df.plot(kind='bar', rot=0, colormap='coolwarm_r', edgecolor='black')
    df.set(xlabel="Residues", ylabel="Residue Frequency (%)")
    df.yaxis.set_major_formatter(mtick.PercentFormatter())

    #df.plot(kind='bar',figsize=(6,6),alpha=0.90,rot=0)
    plt.show()

if __name__ == '__main__':
    Main()