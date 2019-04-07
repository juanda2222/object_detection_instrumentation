import numpy as np
from frecuency_extraction import Frecuency_extraction
from temporal_extraction import Temporal_extract
from energy_extraction import Energy_signal
from get_data import get_data

class Extract_features(Frecuency_extraction,Temporal_extract,Energy_signal):
    pass

#EJEMPLO PARA VER QUE TODO FUNCIONA BIEN 
#Fs = 40000 # frecuencia muestreo
#N = 4000 # numero de datos
#t = np.linspace(0,N/Fs,N) # time vector
#y = 1.5*np.sin(10550.0 * 2.0*np.pi*t) + 4*np.sin((5600.0)* 2.0*np.pi*t)+ 2*np.cos(2020.0 * 2.0*np.pi*t)+ 3*np.cos(4000.0 * 2.0*np.pi*t)+3*np.cos(1000.0 * 2.0*np.pi*t)

#EJEMPLO REAL CON ARDUINO
"""Fs = 8928
s1,s2,s3,s4 = get_data()

signal = Extract_features()

df = signal.frecuency_extraction(s1,Fs)   
dt = signal.temporal_extraction(s1,Fs)
E = signal.energy_extraction(s1)
print("df1: ",df)
print("dt2: ",dt)
print("E1: ",E)

df = signal.frecuency_extraction(s2,Fs)   
dt = signal.temporal_extraction(s2,Fs)
E = signal.energy_extraction(s2)
print("df2: ",df)
print("dt2: ",dt)
print("E2: ",E)

df = signal.frecuency_extraction(s3,Fs)   
dt = signal.temporal_extraction(s3,Fs)
E = signal.energy_extraction(s3)
print("df3: ",df)
print("dt3: ",dt)
print("E3: ",E)

df = signal.frecuency_extraction(s4,Fs)   
dt = signal.temporal_extraction(s4,Fs)
E = signal.energy_extraction(s4)
print("df4: ",df)
print("dt4: ",dt)
print("E4: ",E)

signal.frecuency_graphic(s1,Fs)"""
