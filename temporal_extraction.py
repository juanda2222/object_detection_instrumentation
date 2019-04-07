import numpy as np
import matplotlib.pyplot as plt
from get_data import get_data
from get_vector import get_vector 
class Temporal_extract(object):
    def __init__(self): #método
        print("_______temporal_extraction______")
 
    def resta(self,n,m):
        return n-m
 
    def temporal_extraction(self,y,Fs):
        
        resta = self.resta
        dat = [abs(a) for a in y] 
        max_valor = max(dat)
        valor_min_dat = (max_valor)/4
        valores_max = []
        index_valores_max = []
        v = 0
        for i in dat:
            if i > valor_min_dat:
                valores_max.append(i)
                index_valores_max.append(v)
            v += 1            
        vector_dt = [1/Fs*m for m in index_valores_max.copy()]
        #dt = sum(vector_dt)/len(vector_dt)
        #return dt
        index_valores_max.append(0)
        index_valores_max = [1/Fs*a for a in index_valores_max]
        vector_dt.insert(0,0)
        vector_dt = list(map(resta,index_valores_max,vector_dt))
        vector_dt = vector_dt[1:len(vector_dt)-1]
        dT = sum(vector_dt)/len(vector_dt)
        return dT
        #print("Los máximos valores son: ",valores_max)
        #print("El tiempo de cada pico es: ", index_valores_max[0:len(index_valores_max)-1])
        #print("La diferencia entre cada tiempo es: ",vector_dt)
        #print("dT: ",dT)
 
    def temporal_graphic(self,y,Fs):
        a = 1
        N = len(y)
        xt = np.linspace(0.0, N/(a*Fs), N//a)
        plt.cla()
        plt.plot(xt, y[0:N//a],'k')
        plt.show()

