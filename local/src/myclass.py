#!/home/vince/anaconda2/envs/struct_pred/bin/python

import numpy as np
import pickle

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

    # w is the sliding window size
    w: int

    def __init__(self,w=17):
        self.w = w
        self.res = ['H','E','-']
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
    
    # Serialize the dataset object using the pickle module.
    def dump(self,file):
        with open(file,'wb') as outfile:
            pickle.dump(self.model,outfile)

    # Deserialize a trained model. Load operation should be useful
    # for fast recover of trained models.
    def load(self,file):
        with open(file,'rb') as infile:
            loaded = pickle.load(infile)
        return loaded

    '''
    Define the training procedure according to the GOR method. The train
    method takes in input a Dataset object, then automatically extracts 
    the dssp string and the pssm from the Dataset object. The procedure is
    Iterative and doesn't require any special input encoding.  
    '''
    # Simple training. Returns an updated model containing for each
    # secondary structure element, a matrix storing the result of the counting
    # performed on the Dataset.  
    def train(self,tdata,info=True):  # tdata stands for 'training data'    
        i, j, k = 0, self.w//2, self.w
        for key in tdata:
            dssp = tdata[key][0]; pssm = tdata[key][1]
            while k <= len(dssp):
                self.model[self.res.index(dssp[j])] += pssm[i:k]
                self.sse[self.res.index(dssp[j])] += 1
                i, j, k = i+1, j+1, k+1
            i, j, k = 0, self.w//2, self.w
        self.count = sum(self.sse)
        if info: self._information() # transorm the model content as described in the information method.
        return self
    
    # Normalize the model dividing each matrix for the total number of
    # residues in the Dataset.
    def _normalize(self):
        self.model = self.model/self.count
        self.sse = self.sse/self.count
        self.overall = sum(self.model)
        return self

    # Transform the content of the model from probailities to informations.
    # If the 'info' flag is set to True this method will be called by default by
    # the train method.
    def _information(self):
        self._normalize()
        for val in range(len(self.res)):
            self.model[val] = np.log(self.model[val]/(self.overall*self.sse[val]))
        return self

    '''
    The predict method takes in input a trained model (Gor object) and a Dataset
    object containing at least the pssm. It adds a new value consisting of a
    string of predicted secondary structure assignments for each element present
    in the Dataset.
    '''
    def predict(self,trained,pdata): # trained refers to a trained model and pdata to 'prediction data'
        i, k = 0, self.w
        for key in pdata:
            seq = ''
            pssm = pdata[key][1]
            while k <= len(pssm):
                assignment = np.array([np.sum(trained[h]*pssm[i:k]) for h in range(3)])
                seq += self.res[np.argmax(assignment)]
                i, k = i+1, k+1
            i, k = 0, self.w
            pdata[key].append(seq)
            if pdata[key][0]:
                pdata[key][0] = pdata[key][0].replace('*','') # remove the padding performed on dssp sequence(for test set)
        return pdata



class Svm:
    '''
    Definition of methods allowing the basic operations on Svm's
    class objects.  
    '''

    def __init__(self,w=17):
        self.w = w
        self.classes = {'H':1,'E':2,'-':3}
        self.encoded = ''
    
    # Return the lenght of the object given as argument.
    def __len__(self,obj):
        return len(obj)

    # Allow to iterate over the Dataset object.
    def __iter__(self):
        return iter(self.dataset)

    '''
    Encoding of the inut for SVM training and prediction. The class uses
    Dataset objects. Need at least the sequence profile.
    '''
    # Return a string containing the encoding of all the Dataset members.
    def encode(self,tdata,): # takes in input training or prediction data.
        for key in tdata:
            dssp = tdata[key][0]; pssm = tdata[key][1]
            if self._key_encode(dssp,pssm,key):
                self.encoded += self._key_encode(dssp,pssm,key)
        return self.encoded
        
    # Performs the encoding for a single element in the Dataset. Takes in 
    # input the pssm the dssp and the key of the element.
    def _key_encode(dssp,pssm,key):
        full = ''
        i, j, k = 0, self.w//2, self.w
        while k <= len(pssm):
            h = 1; tmp_str = ''
            for line in pssm[i:k]:
                for val in line:
                    if val:
                        tmp_str += ' %s:%s '%(h,val)
                    h += 1
            if tmp_str: full += '%s\t%s\n'%(self.classes[dssp[j]],tmp_str)
            i, j, k = i+1, j+1, k+1
        return full

    '''
    '''
    def train():
        pass
    def predict():
        pass


class Dataset:
    '''
    Definition of methods allowing the basic operations on Dataset's
    class objects.  
    '''

    # w is window size. path should correspond to a folder 
    # containing pssm and dssp subfolders.
    path: str; w: int

    def __init__(self,w=17,path=''): # path of training or test set folders
        self.w = w
        self.path = path
        self.dataset = {} # this will be our dataset.

    # Return the lenght of the object given as argument.
    def __len__(self,obj):
        return len(obj)

    # Allow to iterate over the Dataset object.
    def __iter__(self):
        return iter(self.dataset)
    
    # Allow slicing operation.
    def __getitem__(self,index):
        return self.dataset[index]

    # Printing options.
    def __str__(self):
        values = ['dssp','pssm','prediction']
        np.set_printoptions(threshold=np.inf)
        return '{0}'.format(self.dataset) # !To improve the printing stuff!
    
    # Allow the additions in the dataset after its generation.
    def add(self,key,default):
        self.dataset[key] = self.dataset.get(key,default)
        return self.dataset

    # Serialize the dataset object using the pickle module.
    def dump(self,filename):
        with open(filename,'wb') as outfile:
            pickle.dump(self.dataset,outfile)
    
    def load(self,file):
        with open(file,'rb') as infile:
            trained = pickle.load(infile)
        return trained

    # Calls all the methods gathering the information necessary
    # to memorize the complete dataset. 
    def getall(self,idlist):
        with open(idlist) as f:
            for val in f:
                val = val.rstrip()
                self.dataset[val] = self.dataset.get(val,[])
                self.dataset[val].append(self._sequence(val))
                self.dataset[val].append(self._profile(val))
        return self

    '''
    Basically the dataset is formed by a list of DSSP secondary structure
    assignments and a list of profiles obtained from a PSIBLAST run.
    Therefore the methods defined in the following section works with those
    type of inputs.
    N.B.: padding of sequences and profiles is also performed. 
    '''

    # Get the DSSP assignment of a given structure as string of
    # characters. If the 'parse' flag is set to True the method
    # _parser will be called.
    def _sequence(self,filename,parse=False):
        with open(self.path+'dssp/'+filename+'.dssp') as f:
            seq = ''
            dssp = str(f.read().splitlines()[1].rstrip())
            if not parse:
                seq += '*'*(self.w//2)+dssp+'*'*(self.w//2)
                return seq
            else: 
                return self._parser(f)

    # Allow to parse a dssp file without any preprocessing required.
    def _parser(self,filename):
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

    # Called only if the 'parse' flag is set to True. Maps an 8 element
    # ss assignment to a 3 element ss assignment.
    def _replace(self,string):
        H = ['H','G','I']
        E = ['B','E']
        C = ['S','T',' ']
        seq = ''
        for ch in sting:
            if ch in C: seq += '-'
            elif ch in E: seq += 'E'
            else: seq += 'H'
        return  seq


    # Read the .pssm file associated to a specific PDB ID, after
    # select only the pseudocounter section, extract the profile
    # and transforms it in a numpy object.
    def _profile(self,filename):
        psiout = []
        pad = np.zeros((self.w//2,20))
        with open(self.path+'pssm/'+filename+'.pssm') as f:
            for line in f:
                line = line.rstrip().split()
                if not line: pass
                elif line[0].isdigit(): psiout.append(line[22:-2])
            matrix = pad
            for line in psiout:
                line = np.array(line).astype(float)
                matrix = np.vstack((matrix,line))      
        matrix = np.vstack((matrix,pad))/100
        return matrix