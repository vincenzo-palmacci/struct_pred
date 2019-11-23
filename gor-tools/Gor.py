#!/home/vince/Desktop/project/local/conda_env/str_prj/bin/python

import pickle
import numpy as np
from Dataset import Dataset

class Gor:
    '''
    Definition of methods allowing the basic operations on Gor's
    class objects.
    The training returns a model consisting of a series of
    numpy arrays (could be saved using the dump method), this phase
    requires a trining Dataset object (pssm and dssp). The prediction
    uses a trained model (can be loaded from a file) and perform 
    the computation over a Dataset object containing one more value
    for each element (predicted secondary structure).
    '''
        
    def __init__(self,w=17):
        self.w = w
        self.res = ['-','E','H']
        self.sse = np.zeros((3))
        self.model = np.zeros((3,self.w,20)) # Initialize the model as 3D tensor.

    # Make the model iterable. Defined mostly for printing and search purposes.
    def __iter__(self):
        return iter(self.model)

    # Print the whole model.
    def __str__(self):
        np.set_printoptions(threshold=np.inf)
        return '{0}'.format(self.model)
    
    # Allows slicing operation on the model.
    def __getitem__(self,index):
        return self.model[index]
    
    # Serialize/Deserialize using the pickle module.
    def dump(self,outfile):
        with open(outfile,'wb') as out:
            pickle.dump(self.model,out)
    @classmethod
    def load(cls,infile):
        with open(infile,'rb') as infile:
            return pickle.load(infile)

    # Pad dssp and pssm according to the window's size.
    def _padding_(self,obj):
        if type(obj) == str:
            pad = '-'*(self.w//2)
            obj = pad+obj+pad
        else:
            pad = np.zeros((self.w//2,20))
            obj = np.vstack((pad,obj,pad))
        return obj

    '''
    Define the training procedure according to the GOR method. The train
    method takes in input a Dataset object, then automatically extracts 
    the dssp string and the pssm from the Dataset object. The procedure is
    Iterative and doesn't require any special input encoding.  
    '''
    # Simple training. Returns an updated model containing for each
    # secondary structure element, a matrix storing the result of the counting
    # performed on the Dataset.  
    def train(self,data):    
        i, j, k = 0, self.w//2, self.w
        for key in data:
            dssp = self._padding_(data[key]['dssp'])
            pssm = self._padding_(data[key]['pssm'])
            while k <= len(dssp):
                if np.sum(pssm[i:k]) != 0:
                    self.model[self.res.index(dssp[j])] += pssm[i:k]
                    self.sse[self.res.index(dssp[j])] += 1
                    i, j, k = i+1, j+1, k+1
                else:
                    i, j, k = i+1, j+1, k+1
            i, j, k = 0, self.w//2, self.w
        self.count = sum(self.sse)
        self._information_() # transform the model content as described in the information method.
        return self
    
    # Normalize the model dividing each matrix for the total number of
    # residues in the Dataset.
    def _normalize_(self):
        self.model = self.model/self.count
        self.sse = self.sse/self.count
        self.overall = sum(self.model)
        return self.model

    # Transform the content of the model from probailities to informations.
    # If the 'info' flag is set to True this method will be called by default by
    # the train method.
    def _information_(self):
        self._normalize_()
        for val in range(len(self.res)):
            self.model[val] = np.log(self.model[val]/(self.overall*self.sse[val]))
        return self.model

    '''
    The predict method takes in input a trained model (Gor object) and a Dataset
    object containing at least the pssm. It adds a new value consisting of a
    string of predicted secondary structure assignments for each element present
    in the Dataset.
    ''' 
    def predict(self,trained,data) -> None: # trained refers to a trained model and pdata to 'prediction data'
        prediction = {}
        i, k = 0, self.w
        for key in data:
            seq = ''
            pssm = self._padding_(data[key]['pssm'])
            while k <= len(pssm):
                assignment = np.array([np.sum(trained[h]*pssm[i:k]) for h in range(3)])
                seq += self.res[np.argmax(assignment)]
                i, k = i+1, k+1
            i, k = 0, self.w
            prediction[key] = prediction.get(key,seq)
        data.add(prediction,'GOR')