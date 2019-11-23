#!/home/vince/Desktop/project/local/conda_env/str_prj/bin/python

'''
Plot the composition of the residues.
'''

from Dataset import Dataset
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import numpy as np

def res_count(dataset):
    sse = {'H':0, 'E':0, '-':0}
    for key in dataset:
        for val in sse.keys():
            sse[val] += dataset[key]['dssp'].count(val)
    return pd.DataFrame(sse,index=[0]).T

def Main():
    parser = argparse.ArgumentParser(description='Dataset computing procedure. v1.0')
    parser.add_argument('-d',dest='dataset',type=str,required=True,\
        help='input dataset')

    args = parser.parse_args()

    dataset = Dataset.load(args.dataset)

    df =  res_count(dataset).T
    colors = plt.get_cmap('coolwarm_r')
    labels = ['Helix','Strand','Coil']
    temp = np.array((df['H'],df['E'],df['-']))
    sizes = [i for i in (temp/np.sum(temp))*100]
    #print sizes
    # create a circle for the center of the plot
    my_circle=plt.Circle( (0,0), 0.5, fc='white', edgecolor='black')     
    # compute the pieplot give color names
    fig1, ax1 = plt.subplots()
    ax1.set_prop_cycle("color", [colors(1. * i / len(sizes))
                                        for i in range(len(sizes))])
    plt.pie(df,wedgeprops={"edgecolor":"k", 'linewidth': 1, 'linestyle': 'solid', 'antialiased': True})
    plt.legend( loc='lower right',
                labels=['%s = %1.1f%%' %(l,s) for l,s in zip(labels,sizes)],
                prop={'size': 9},
                bbox_to_anchor=(1, 0),
                bbox_transform=fig1.transFigure)
    p=plt.gcf()

    ax1.axis('equal')
    #plt.title('Composition in Secondary Structure', fontname="Times New Roman", fontweight="bold")
    
    # add the white cyrcle in the middle
    p.gca().add_artist(my_circle)
    plt.show()

if __name__ == '__main__':
    Main()