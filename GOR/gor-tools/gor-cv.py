#!/home/vince/Desktop/project/local/conda_env/str_prj/bin/python

from Tools import Dataset,Gor
import sys
import pickle

data_path = '/home/vince/Desktop/project/dataset/training/'
cv_path = '/home/vince/Desktop/project/dataset/cv/'

def cv_training(train_list):
    training_data = Dataset(path=data_path).getall(train_list)
    trained = Gor().train(training_data)
    return trained

def cv_test(model,test_inlist):
    test_data = Dataset(path=data_path).getall(test_list)
    prediction = Gor().predict(model,test_data)
    return prediction

if __name__=='__main__':
    for val in range(1,5):
        train_list= cv_path+'/fold%r/cv_train.id'%(val)
        test_list = cv_path+'/fold%r/cv_test.id'%(val)
        trained = cv_training(train_list)
        prediction = cv_test(trained,test_list)
        with open('cv'+str(val)+'_pred'+'.pickle','wb') as outfile:
            pickle.dump(prediction,outfile,protocol=pickle.HIGHEST_PROTOCOL)