import numpy as np
class Energy_signal(object):
    def __init__(self):
        print("_______energy_extaction______")
  
    def energy_extraction(self,y):
        result = [x*x for x in y]
        energia=sum(result)
        return energia

