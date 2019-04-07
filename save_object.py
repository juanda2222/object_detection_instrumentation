import numpy
import csv
from pandas import read_csv

def save_object(dF,dT,E,Object):

    myData =[[dF,dT,E,Object]]

    myFile = open('data.csv','a')

    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(myData)
        
    print("Writing complete")

def read_object():

    dataframe = read_csv("data.csv", header=None)
    dataset = dataframe.values
    X = dataset[:,0:3].astype(float)
    y = dataset[:,3]

