from scipy.fftpack import fft
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
from get_data import get_data

class Frecuency_extracion(object):
    def __init__(self): #método
        print("_______frecuncy_extraction______")

    def resta(self,n,m):
        return n-m

    def extracion(self,yf,N):
        resta = self.resta
        dat = [abs(yf) for yf in yf.tolist()] # convertir yf a lista
        data_norm = 2.0/N * np.abs(dat[0:N//2])
        max_valor = max(2.0/N * np.abs(dat[0:N//2]))
        min_valor = min(2.0/N * np.abs(dat[0:N//2]))
        valor_min_dat = (max_valor+min_valor)/6
        valores_max = []
        index_valores_max = []
        v = 0
        for i in data_norm:
            if i > valor_min_dat:
                valores_max.append(i)
                index_valores_max.append(v)
            v += 1
        df = index_valores_max.copy()
        index_valores_max.append(0)
        df.insert(0,0)
        df = list(map(resta,index_valores_max,df))
        dF = df[1:len(df)-1]
        print("Los máximos valores normalizados son: ",valores_max)
        print("Las frecuencias de cada pico son: ",index_valores_max[0:len(index_valores_max)-1])
        print("La diferencia entre cada frecuencia es: ",dF)

    def graphic(self,N,T,yf,y):

        xf1 = np.linspace(0.0, 1.0/(2.0*T), N)
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
        plt.subplot(2,1,1)
        plt.cla()
        plt.plot(xf1, y[0:N],'b')
        plt.grid()
        plt.subplot(2,1,2)
        plt.cla()
        plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]),'r')
        plt.draw()
        plt.pause(6)

#serial,a,b,c = get_data()
#N1 = len(serial)
#T1 = 1.0/N1

#EJEMPLO PARA VER QUE TODO FUNCIONA BIEN 
N = 1000
T = 1.0/N
x = np.linspace(0.0,N*T,N)
y = 5*np.sin(35.0 * 2.0*np.pi*x) + np.sin((380.0)* 2.0*np.pi*x)+ 2*np.cos(120.0 * 2.0*np.pi*x)+ 3*np.cos(80.0 * 2.0*np.pi*x)
yf= fft(y)
frecuencia = Frecuency_extracion()
frecuencia.extracion(yf,N)
frecuencia.graphic(N,T,yf,y)


