from extract_features import Extract_features
from get_vector import get_vector
Fs = 8928
y = get_vector()

signal = Extract_features()

dF = signal.frecuency_extraction(y,Fs)   
dt = signal.temporal_extraction(y,Fs)
E = signal.energy_extraction(y)
print(dF)
print(dt)
print(E)
signal.frecuency_graphic(y,Fs)