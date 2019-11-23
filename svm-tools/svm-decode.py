#!/home/vince/Desktop/project/local/conda_env/str_prj/bin/python

from Dataset import Dataset
import argparse

mapper = {1:'H',2:'E',3:'-'}

def testing(data,infile):
    prediction = {}
    for key in data:
        seq = ''
        while len(seq) < len(data[key]['dssp']):
            encoded = int(infile.pop(0).rstrip())
            seq += mapper[encoded]
        prediction[key] = prediction.get(key,seq)
    data.add(prediction,'SVM')
    return data

def Main():
    parser = argparse.ArgumentParser(description='Vincenzo 21/11/2019: SVM output decoding. v1.1')
    parser.add_argument('-d',dest='dataset',type=str,required=True,\
        help='dataset object to be loaded for the encoding')
    parser.add_argument('-i','--in',dest='infile',type=str,required=True,\
        help='specify an input file containing the predictions.')
    parser.add_argument('-o','--out',dest='out',type=str,required=True,\
        help='specify an ouput file.')

    args = parser.parse_args()
    data = Dataset.load(args.dataset) ; infile = open(args.infile).readlines()

    prediction = testing(data,infile)

    prediction.dump(args.out+'.dat')
    return print('SVM-decoding succesfully saved at %r'%(args.out+'.dat'))

if __name__=='__main__':
    Main()
