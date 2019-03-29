import numpy as np
import matplotlib.pyplot as plt
from get_vector import get_vector
class Energy_signal(object):
    def __init__(self): #método
        print("_______energy_extaction______")
    def cuadrado(self,n): 
        return n**2 
  
    def energy_extraction(self,y):
        cuadrado = self.cuadrado
        result =map(cuadrado, y)
        energia=sum(result)
        return energia
        #print("E: ",energia)
