from scipy.fftpack import fft
import numpy as np
import matplotlib.pyplot as plt
from get_data import get_data
from get_vector import get_vector

class Frecuency_extracion(object):
    def __init__(self): #método
        print("_______extraction_features______")

    def resta(self,n,m):
        return n-m

    def frecuency_extraction(self,y,Fs):
        yf = fft(y)
        N = len(yf)
        resta = self.resta
        dat = [abs(yf) for yf in yf.tolist()] # convertir yf a lista
        data_norm = 2.0/N * np.abs(dat[0:N//2])
        max_valor = max(2.0/N * np.abs(dat[0:N//2]))
        min_valor = min(2.0/N * np.abs(dat[0:N//2]))
        valor_min_dat = (max_valor+min_valor)/4
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
        plt.plot(xf1, y[0:N//a],color = [0.0134,0.023,0.0845])
        plt.xlabel("time(s)")
        plt.subplot(2,1,2)
        plt.cla()
        plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]), color = [0.0334,0.213,0.245])
        plt.xlabel("frecuency(Hz)")
        plt.show()


#EJEMPLO PARA VER QUE TODO FUNCIONA BIEN 
#Fs = 8000 # frecuencia muestreo
#N = 1000 # numero de datos
#t = np.linspace(0,N/Fs,N) # time vector
#y = 1.5*np.sin(2550.0 * 2.0*np.pi*t) + 4*np.sin((3600.0)* 2.0*np.pi*t)+ 2*np.cos(2020.0 * 2.0*np.pi*t)+ 3*np.cos(800.0 * 2.0*np.pi*t)+3*np.cos(1000.0 * 2.0*np.pi*t)

#f = Frecuency_extracion()
#f.frecuency_graphic(y,Fs)
#f.frecuency_extraction(y,Fs)


