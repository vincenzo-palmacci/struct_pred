#!/home/vince/Desktop/project/local/conda_env/str_prj/bin/python

import pickle
from collections import OrderedDict
import sys
import numpy as np
import pandas as pd
import random

class Dataset:

    def __init__(self,title):
        self.dataset = OrderedDict()
        self.title = title

    # Allow to iterate over the object.
    def __iter__(self):
        return iter(self.dataset)

    # Allow slicing operation.
    def __getitem__(self,index):
        return self.dataset[index]
    
    # Return the lenght.
    def __len__(self,obj):
        return len(obj)

    # Print options.
    def __str__(self):
        np.set_printoptions(threshold=np.inf)
        return '{0}'.format(self.dataset)
    ## Show a specific field in a pretty format.    
    def show(self,val_type):
        np.set_printoptions(threshold=np.inf)
        for key in self.dataset:
            print('>{0}\n{1}'.format(key,self.dataset[key][val_type]))

    # Serialize/Deserialize the Dataset using the pickle module.
    def dump(self,outfile):
        with open(outfile,'wb') as out:
            pickle.dump(self.dataset,out)
    @classmethod
    def load(cls,filename):
        with open(filename,'rb') as infile:
            obj = pickle.load(infile)
        return cls._fetch_dataset_(obj,filename)

    # Transform a dictionary of dictionaries in a Dataset
    @classmethod
    def _fetch_dataset_(cls,obj,filename):
        dataset = Dataset(filename)
        title_dict = cls._split_(obj)
        for val in title_dict:
            dataset.add(val[1],val[0])
        return dataset
    
    # Split a dictionary of dictionaries.
    @classmethod
    def _split_(cls,obj):
        rand_key = random.choice(list(obj.keys()))
        title_dict = []
        for val in obj[rand_key]:
            title_dict.append((val,dict((i,obj[i][val])for i in obj)))
        return title_dict

    # Save the Dataset as comma separated file.
    def to_csv(self):
        df = pd.DataFrame(self.dataset).T
        df.to_csv(self.title+'.csv')

    # Add features to the Dataset. By now can add Profile and 
    # Sequence classes objects.
    def add(self,obj,val_name):
        for key in obj:
            self.dataset[key] = self.dataset.get(key,{val_name:None})
            self.dataset[key][val_name] = obj[key]
        return self

    # Core method of the class: build a dataset starting from
    # different objects.
    @classmethod
    def build(cls,title,*kwargs):
        dataset = Dataset(title)
        for arg in kwargs:
            dataset.add(arg,arg.title)
        return dataset


class Profile:
    
    def __init__(self):
        self.dataset = OrderedDict()
        self.title = 'pssm'

    # Allow to iterate over the object.
    def __iter__(self):
        return iter(self.dataset)
    
    # Allow slicing operation.
    def __getitem__(self,index):
        return self.dataset[index]
    
    # Return the lenght.
    def __len__(self,obj):
        return len(obj)

    # Print options.
    def __str__(self):
        np.set_printoptions(threshold=np.inf)
        return '{0}'.format(self.dataset)

    # Read the .pssm file associated to a specific PDB ID, select 
    # only the pseudocounter section, extract the profile
    # and transforms it in a numpy object.
    @staticmethod
    def _psiblast_(path,filename):
        psiout, matrix = [], []
        with open(path+'pssm/'+filename+'.pssm') as f:
            for line in f:
                line = line.rstrip().split()
                if not line: pass
                elif line[0].isdigit(): psiout.append(line[22:-2])
            for line in psiout:
                line = np.array(line).astype(float)
                matrix.append(line)      
        matrix = np.array(matrix)/100
        return matrix
    
    # Build a dictionary where each key is a PDB ID and
    # the values are profiles. By now only PSIBLAST 
    # profiles can be parsed and used.
    def get_dict(self,path,inlist,prof_type):
        with open(inlist) as ids:
            for val in ids:
                val = val.rstrip()
                self.dataset[val] = self.dataset.get(val)
                if prof_type == 'psiblast':
                    self.dataset[val] = self._psiblast_(path,val)
        return self
    

class Sequence:

    def __init__(self):
        self.title = None
        self.dataset = OrderedDict()

    # Allow to iterate over the object.
    def __iter__(self):
        return iter(self.dataset)
    
    # Allow slicing operation.
    def __getitem__(self,index):
        return self.dataset[index]
    
    # Return the lenght.
    def __len__(self,obj):
        return len(obj)

    # Print options.
    def __str__(self):
        return '{0}'.format(self.dataset)

    # Allow to parse a dssp file without any preprocessing required.
    @staticmethod
    def _raw_dssp_(filename):
        seq = ''
        flag = 0
        for line in filename:
            if line.find('  #  RESIDUE') == 0:
                flag = 1
                continue
            if flag == 1:
                if line[11] == chain:
                    seq += (line[16])
        seq = self._replace(seq)
        return seq

    # Get the DSSP assignment of a given structure as string of
    # characters. If the 'parse' flag is set to True the method
    # _parser_ will be called.
    @staticmethod
    def _dssp_(path,filename,parse=False):
        with open(path+'dssp/'+filename+'.dssp') as f:
            seq = ''
            dssp = str(f.read().splitlines()[1].rstrip())
            if not parse:
                seq += dssp
                return seq
            else:
                return self._raw_dssp_(f)

    # Get the fasta sequence.
    @staticmethod
    def _fasta_(path,filename,parse=False):
        with open(path+'fasta/'+filename+'.fasta') as f:
            seq = ''
            seq = str(f.read().splitlines()[1].rstrip())
        return seq

    # Build a dictionary where each key is a PDB ID and
    # the values are sequences. By now only FASTA and DSSP 
    # can be parsed and used.
    def get_dict(self,path,inlist,seq_type):
        self.title = seq_type
        with open(inlist) as ids:
            for val in ids:
                val = val.rstrip()
                self.dataset[val] = self.dataset.get(val)
                if seq_type == 'dssp':
                    self.dataset[val] = self._dssp_(path,val)
                elif seq_type == 'fasta':
                    self.dataset[val] = self._fasta_(path,val)
        return self