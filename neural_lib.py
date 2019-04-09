from pandas import read_csv
import numpy as np
from sklearn.preprocessing import LabelEncoder

# this may take a while
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier

import numpy
import csv
from pandas import read_csv

class Neural_lib(object):
    def __init__(self, neuralName = "superNeural", numIn = 3):

        self.neuralName = neuralName
        self.numIn = numIn # number of inputs
        self.mlp = None # this is my classifier
        self.scaler = None # used to scale the input data

    def save_data_file(self, x, y='none'):
        assert x == []
        myData =[[x.append(y)]]
        myFile = open(self.neuralName + '_data.csv','a') # always add new line 'w' to overwrite
        with myFile:
            writer = csv.writer(myFile)
            writer.writerows(myData)
        print("Writing complete")

    def errase_data_file(self):

        myFile = open(self.neuralName + '_data.csv','w') # always add new line 'w' to overwrite
        with myFile:
            writer = csv.writer(myFile)
            writer.writerows([])
        print("errased complete complete")


    def read_data_file(self, numIn):

        dataframe = read_csv(self.neuralName + '_data.csv', header=None) # this is a csv object tor sheets processing
        dataset = dataframe.values # this is a numpy 2 d array 
        x = dataset[:,0:numIn].astype(float) # use only the numbers (input)
        y = dataset[:,numIn] # take the output 
        #print(x) 
        #print(y)
        return x, y


    def train_neural_network(self):

        x, y = self.read_data_file(self.numIn) 
        X_train, X_test, y_train, y_test = train_test_split(x, y) # use randomply data to get the input and output
        
        # get a report of the current performance of the neural
        #predictions = mlp.predict(X_test)
        #from sklearn.metrics import classification_report
        #print(classification_report(y_test,predictions))

        # normalize the input data
        self.scaler = StandardScaler() # create the scaller
        self.scaler.fit(X_train) # adjust the scaller
        X_train = self.scaler.transform(X_train) # scale input
        X_test = self.scaler.transform(X_test)  # scale input
        
        #mlp=MLPClassifier(hidden_layer_sizes=(10,10,10), max_iter=500, alpha=0.0001,
        #                    solver='adam', random_state=21,tol=0.000000001)
        
        # train the classifier
        self.mlp = MLPClassifier(hidden_layer_sizes=(6,6,6,6),solver='lbfgs',max_iter=6000)
        self.mlp.fit(X_train,y_train)

    def predict_neural_network(self, x):

        x_scaled = self.scaler.transform([x]) # scale 
        predictions_str = self.mlp.predict(x_scaled) 
        print(predictions_str[0]) # order the most likeley prediction (the first is the most likeley)
        predictions = self.mlp.predict_proba(x_scaled) # give us the probability of the outputs
        print(predictions) # the first level is the percentage an the subsecuents in order
        
        return predictions[0, 0]*100, predictions[0, 1]*100, predictions[0,2]*100, predictions_str[0] # object 1, object 2 ... name_of_object (prediction)
        
