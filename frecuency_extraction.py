from scipy.fftpack import fft
import numpy as np
import matplotlib.pyplot as plt
from get_data import get_data

class Frecuency_extraction(object):
    def __init__(self): #método
        print("_______extraction_features______")

    def resta(self,n,m):
        return n-m

    def frecuency_extraction(self,y,Fs):
        resta = self.resta
        yf = fft(y)
        N = len(yf)
        dat = [abs(yf) for yf in yf.tolist()] # convertir yf a lista
        data_norm = np.abs(dat[0:N//2])*2/N
        max_valor = max(np.abs(dat[0:N//2])*2/N)
        valor_min_dat = (max_valor)/10
        valores_max = []
        index_valores_max = []
        v = 0
        for i in data_norm:
            if i > valor_min_dat:
                valores_max.append(i)
                index_valores_max.append(v*Fs/N)
            v += 1            
        vector_df = index_valores_max.copy()
        index_valores_max.append(0)
        vector_df.insert(0,0)
        vector_df = list(map(resta,index_valores_max,vector_df))
        vector_df = vector_df[1:len(vector_df)-1]
        #return vector_df
        dF = sum(vector_df)/len(vector_df)
        return dF
        #print("Los máximos valores normalizados son: ",valores_max)
        #print("Las frecuencias de cada pico son: ",index_valores_max[0:len(index_valores_max)-1])
        #print("La diferencia entre cada frecuencia es: ",vector_df)
        #print("dF: ",dF)

    def frecuency_graphic(self,y,Fs):
        a = 1
        N = len(y)
        yf = fft(y)
        xf1 = np.linspace(0.0, N/(a*Fs), N//a)
        xf = np.linspace(0.0, Fs/(2.0), N//2)
        plt.subplot(2,1,1)
        plt.cla()
        plt.plot(xf1, y[0:N//a],'k')#color = [0.134,0.43,0.1845])
        plt.xlabel("time(s)")
        plt.subplot(2,1,2)
        plt.cla()
        plt.plot(xf,np.abs(yf[0:N//2])*2/N, 'r')# color = [0.114,0.313,0.285])
        plt.xlabel("frecuency(Hz)")
        plt.show()


#EJEMPLO PARA VER QUE TODO FUNCIONA BIEN 
#Fs = 8000 # frecuencia muestreo
#N = 1000 # numero de datos
#t = np.linspace(0,N/Fs,N) # time vector
#y = 1.5*np.sin(2550.0 * 2.0*np.pi*t) + 4*np.sin((3600.0)* 2.0*np.pi*t)+ 2*np.cos(2020.0 * 2.0*np.pi*t)+ 3*np.cos(800.0 * 2.0*np.pi*t)+3*np.cos(1000.0 * 2.0*np.pi*t)
#
#f = Frecuency_extraction()
#f.frecuency_graphic(y,Fs)
#a = f.frecuency_extraction(y,Fs)
#print(a)

