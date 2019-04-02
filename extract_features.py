import numpy as np
from frecuency_extraction import Frecuency_extracion
from temporal_extraction import Temporal_extract
from energy_extraction import Energy_signal
from get_vector import get_vector

class Extract_features(Frecuency_extracion,Temporal_extract,Energy_signal):
    pass

#EJEMPLO PARA VER QUE TODO FUNCIONA BIEN 
#Fs = 40000 # frecuencia muestreo
#N = 4000 # numero de datos
#t = np.linspace(0,N/Fs,N) # time vector
#y = 1.5*np.sin(10550.0 * 2.0*np.pi*t) + 4*np.sin((5600.0)* 2.0*np.pi*t)+ 2*np.cos(2020.0 * 2.0*np.pi*t)+ 3*np.cos(4000.0 * 2.0*np.pi*t)+3*np.cos(1000.0 * 2.0*np.pi*t)

#EJEMPLO REAL CON ARDUINO
Fs = 8928
y = get_vector()

signal = Extract_features()
df = signal.frecuency_extraction(y,Fs)   
dt = signal.temporal_extraction(y,Fs)
E = signal.energy_extraction(y)

print("df: ",df)
print("dt: ",dt)
print("E: ",E)
signal.frecuency_graphic(y,Fs)