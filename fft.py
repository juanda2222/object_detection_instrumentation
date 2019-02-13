from scipy.fftpack import fft
import numpy as np
import matplotlib.pyplot as plt
from time import sleep

N = 600
T = 1.0/800.0
#print(x)

for i in range(1,100):
   
    x = np.linspace(0.0,N*T,N)
    y = np.sin(i*50.0 * 2.0*np.pi*x) + 0.5*np.sin((380.0//i) * 2.0*np.pi*x)+ np.cos(i*120.0 * 2.0*np.pi*x)
    #y =  np.sin(2.0*np.pi*x) 
    yf = fft(y)
    xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
    plt.subplot(2,1,1)
    plt.cla()
    plt.plot(xf, y[0:N//2],'b')
    plt.grid()
    plt.subplot(2,1,2)
    plt.cla()
    plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]),'r')
   
    #plt.ion() 
    #plt.isinteractive()
    #plt.show()
    plt.draw()
    plt.pause(0.0001)
    #input("Press [enter] to continue.")
    #plt.show(block = False)
    #plt.show()
    #sleep(2)
    #plt.close()
