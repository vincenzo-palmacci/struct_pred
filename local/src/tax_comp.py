#!/home/vince/anaconda2/envs/lab2/bin/python

'''
From a csv file obtained after an advanced search on the PDB, 
plot a piechart of the taxonomic composition.
Working directory: pre_statistics
'''

import pandas as pd
import matplotlib.pyplot as plt
import sys

def pretty_dic(d):
    for key in d:
        print (key,':',d[key])

def count_species(intable):
    d = {}
    df = pd.read_csv(intable) # transform the inpt table into a DataFrame
    
    # start count the species in the table
    for sp in df['Source']:
        d[sp] = d.get(sp, 0)
        d[sp] += 1
    
    total = sum(list(d.values()))

    # gather the least frequent species in a single key of the dictionary
    d['other'] = 0
    l = []
    for key in d:
        if d[key]/total < 0.02:
            d['other'] += d[key]
            l.append(key)
    
    # delete the key that are no more necessary 
    for i in l:
        del d[i]

    return d

def pie_spec(d):
    tot = sum(list(d.values()))
    data = [i/tot for i in list(d.values())]
    labels = list(d.keys())
    colors = ['C0','C1','C2','C3']

    # compute the pieplot give color names
    fig1, ax1 = plt.subplots()
    ax1.pie(data, colors = colors, labels=labels, autopct='%1.1f%%', startangle=90)
        
    #draw circle
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # Equal aspect ratio ensures that pie is drawn as a circle
    ax1.axis('equal')
    plt.title('Species composition', fontname="Times New Roman", fontweight="bold")
    #plt.show()
    plt.show()
    
if __name__ == '__main__':
    
    try:
        intable = sys.argv[1] # table downloaded from the PDB
    except:
        print ('Usage: script.py <pdb>.csv')
        raise SystemExit
    else:
        D = count_species(intable) # dictionary containing the species count
        pretty_dic(D)

        # compute plot the pie chart
        pie_spec(D)