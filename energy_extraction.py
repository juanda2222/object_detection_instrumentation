import numpy as np
import matplotlib.pyplot as plt
from get_vector import get_vector
class energy_signal(object):
    def __init__(self): #método
        print("_______energy_extaction______")
    def cuadrado(self,n): 
        return n**2 
  
    def extracion(self,y):
        cuadrado = self.cuadrado
        result =map(cuadrado, y)
        sumatoria=sum(result)
        print(sumatoria)

#EJEMPLO PARA VER QUE TODO FUNCIONA BIEN 
#Fs = 8000 # frecuencia muestreo
#N = 1000 # numero de datos
#t = np.linspace(0,N/Fs,N) # time vector
#y = 1.5*np.sin(2550.0 * 2.0*np.pi*t) + 4*np.sin((3600.0)* 2.0*np.pi*t)+ 2*np.cos(2020.0 * 2.0*np.pi*t)+ 3*np.cos(800.0 * 2.0*np.pi*t)+3*np.cos(1000.0 * 2.0*np.pi*t)

#EJEMPLO CON DATOS TOMADOS CON ARDUINO
y = get_vector()


energy = energy_signal()
energy.extracion(y)