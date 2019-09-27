import numpy as np
import pickle

class database:

    ## General methods for database class. 
    def __init__(self,w=17):
        self.w = w
        self.stack = []

    def __len__(self):
        return len(self.obj)

    def push(self,obj):
        return self.stack.append(obj)

    def pop(self):
        return self.stack.pop()
    
    def notEmpty(self):
        return self.stack != []
    
    def Pickle(self,obj,file)
        with open(file,'wb') as outfile:
            pickle.dump(obj,oufile)


    ## Methods specific for working with dssp files (parsed or not).
    def sequence(self,filename,parse=False):
        with open('dssp/'+filename+'.dssp') as f:
            seq = ''
            if not parse:
                seq += '*'*(self.w//2)+str(f.read().splitlines()[1].rstrip())+'*'*(self.w//2)
            else: 
                self.parser(f)

    def parser(self,filename)
        seq = ''
        flag = 0
        for line in filename:
            if line.find('  #  RESIDUE') == 0:
                flag = 1
                continue
            if flag == 1:
                if line[11] == chain:
                    seq += (line[16])
        seq = self.replace(seq)
        return seq

    def replace(self,string):
        H = ['H','G','I']; E = ['B','E']; C = ['S','T',' ']
        seq = ''
        for ch in sting:
            if ch in C: seq += '-'
            elif ch in E: seq += 'E'
            else: seq += 'H'
        return  seq

    def stack_seq(self,idlist):
        with open(idlist) as f:
            for val in f:
                val = val.rstrip()
                self.stack.append(self.sequence(val))


    ## Methods specific for working with Psiblast pssm output files.
    def profile(self,filename):
        psiout = []
        with open('pssm/'+filename+'.pssm') as f:
            for line in f:
                line = line.rstrip().split()
                try: line[0]
                except: pass
                else:
                    if line[0].isdigit():
                        psiout.append(line[22:-2])
            matrix = self.pad
            for line in psiout:
                line = np.array(line).astype(float)
                matrix = np.vstack((matrix,line))
            
        matrix = np.vstack((matrix,self.pad))
        matrix /= 100
        return matrix

    def stack_prof(self,idlist):
        with open(idlist) as f:
            for val in f:
                val = val.rstrip()
                self.stack.append(self.profile(val))    




if __name__=='__main__':
    import sys

    profiles = database(); structures = dssp()
    profiles.stack_prof(sys.argv[1]); structures.stack_seq(sys.argv[1])
    model = gor()
    model.train(profiles,structures)

    model.get_info()
    np.set_printoptions(threshold=np.inf)
    print(model)