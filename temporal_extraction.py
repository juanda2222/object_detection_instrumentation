import numpy as np
import matplotlib.pyplot as plt
from time import sleep
from get_data import get_data

class temporal_extract(object):
    def __init__(self): #método
        print("_______temporal_extraction______")
 
    def resta(self,n,m):
        return n-m
 
    def extracion(self,y,Fs):
        
        resta = self.resta
        dat = [abs(a) for a in y] # convertir yf a lista
        max_valor = max(dat)
        min_valor = min(dat)
        valor_min_dat = (max_valor+min_valor)/1.2
        valores_max = []
        index_valores_max = []
        v = 0
        for i in dat:
            if i > valor_min_dat:
                valores_max.append(i)
                index_valores_max.append(v)
            v += 1            
        dt = [1/Fs*m for m in index_valores_max.copy()]
        index_valores_max.append(0)
        index_valores_max = [1/Fs*a for a in index_valores_max]
        dt.insert(0,0)
        dt = list(map(resta,index_valores_max,dt))
        dT = dt[1:len(dt)-1]
        print("Los máximos valores son: ",valores_max)
        print("El tiempo de cada pico es: ", index_valores_max[0:len(index_valores_max)-1])
        print("La diferencia entre cada tiempo es: ",dT)
 
    def graphic(self,y,Fs):
        a = 1
        N = len(y)
        xt = np.linspace(0.0, N/(a*Fs), N//a)
        plt.cla()
        plt.plot(xt, y[0:N//a],'k')
        plt.show()
#y,a,b,c = get_data()

#EJEMPLO PARA VER QUE TODO FUNCIONA BIEN 
Fs = 8000 # frecuencia muestreo
N = 1000 # numero de datos
t = np.linspace(0.0,N/Fs,N)
y = 1.5*np.sin(2550.0 * 2.0*np.pi*t) + 4*np.sin((3600.0)* 2.0*np.pi*t)+ 2*np.cos(2020.0 * 2.0*np.pi*t)+ 3*np.cos(800.0 * 2.0*np.pi*t)+3*np.cos(1000.0 * 2.0*np.pi*t)
tiempo = temporal_extract()
tiempo.extracion(y,Fs)
tiempo.graphic(y,Fs)
