#!/home/vince/anaconda2/envs/lab2/bin/python

'''
Plot the composition in secondary structure of the dataset analyzed.
Working directory: pre_statistics
'''

import matplotlib.pyplot as plt
import sys 

# count how many time each sse occurs in the whole dataset
def Main(indssp):
    D = {}
    for line in indssp:
        line = line.rstrip()
        for ch in line:
            if ch == '-':
                ch = 'C'
            D[ch] = D.get(ch, 1)
            D[ch] += 1

    return D 

# based on the output of the previous function plot a donut plot of the composition
def donut_comp(D):
    tot = sum(list(D.values()))
    data = [i/tot for i in list(D.values())]
    labels = list(D.keys())
    colors = ['C0','C1','C2','C3']
    
    # create a circle for the center of the plot
    my_circle=plt.Circle( (0,0), 0.7, color='white')     
    # compute the pieplot give color names
    fig1, ax1 = plt.subplots()
    plt.pie(data, colors = colors, labels = labels, autopct = '%1.1f%%')
    p=plt.gcf()

    ax1.axis('equal')
    plt.title('Structural composition', fontweight="bold")
    
    # add the white cyrcle in the middle
    p.gca().add_artist(my_circle)
    plt.show()

if __name__ == '__main__':
    try:
        MULTI_DSSP = sys.argv[1] # file containing listed dssp assignment
    except:
        print ('Usage: script.py <listedfile>.dssp')
        raise SystemExit
    else:
        with open(sys.argv[1]) as indssp:
            counted = Main(indssp) 
            donut_comp(counted)