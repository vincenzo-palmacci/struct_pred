#!/home/vince/Desktop/project/local/conda_env/str_prj/bin/python

import pandas as pd
import matplotlib.pyplot as plt
import sys

def scop_domain(inclass):
    s = {}
    for line in inclass:
        line = line.rstrip().split('\t')
        if len(line) > 2:
            if len(line[2]) == 1:
                s[line[2]] = s.get(line[2], line[4])
    
    return s

def map_domain(indssp, inscop, dic):
    d = {}
    for line in inscop:
        line = line.rstrip().split('\t')
        if len(line) > 2:
            dom = line[0]
            scop = line[3]
            d[dom] = scop[0]

    m = {}

    for line in indssp:
        if line.rstrip() in d.keys():
            m[d[line.rstrip()]] = m.get(d[line.rstrip()], 0)
            m[d[line.rstrip()]] += 1
    
    for key in list(dic.keys()):
        if key in list(m.keys()):
            m[dic[key]] = m.pop(key)

    return m

def donut_scop(d):
    tot = sum(list(d.values()))
    data = [i/tot for i in list(d.values())]
    labels = list(d.keys())
    colors = ['C0','C1','C2','C3']
    
    # create a circle for the center of the plot
    my_circle=plt.Circle( (0,0), 0.7, color='white')     
    # compute the pieplot give color names
    fig1, ax1 = plt.subplots()
    plt.pie(data, colors = colors, labels = labels, autopct = '%1.1f%%')
    p=plt.gcf()

    ax1.axis('equal')
    plt.title('SCOP composition', fontname="Times New Roman", fontweight="bold")
    
    # add the white cyrcle in the middle
    p.gca().add_artist(my_circle)
    plt.show()

if __name__ == '__main__':
    indssp = open(sys.argv[1]) # takes as input the output of a simple bash script
    inscop = open(sys.argv[2])
    inclass = open(sys.argv[3])
    dic = scop_domain(inclass)
    print (dic)
    codes = map_domain(indssp, inscop, dic)
    donut_scop(codes)