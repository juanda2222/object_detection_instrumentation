import matplotlib.pyplot as plt
import numpy as np
# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api

Fs = 200.0;  # sampling rate
Ts = 1.0/Fs; # sampling interval
t = np.arange(0,1,Ts) # time vector

ff = 5;   # frequency of the signal
y = np.sin(2*np.pi*ff*t)+2*np.sin(2*np.pi*40*t)

n = len(y) # length of the signal
k = np.arange(n)
print(k)
T = n/Fs
frq = k/T # two sides frequency range
frq = frq[range(n//2)] # one side frequency range

Y = np.fft.fft(y)/n # fft computing and normalization
print(type(Y))
Y = Y[range(n//2)]
plt.subplot(2,1,1)
plt.plot(t,y,'r')
plt.subplot(2,1,2)
plt.plot(frq, abs(Y),'b')
plt.show()

def frecuency(self,y,Fs):
        n = len(y)
        k = np.arange(n)
        T = n/Fs
        frq = k/T
        frq = frq[range(n//2)]
        Y = np.fft.fft(y)/n # fft computing and normalization
        Y = Y[range(n//2)]
        plt.subplot(2,1,1)
        plt.plot(t,y,'r')
        plt.subplot(2,1,2)
        plt.plot(frq, abs(Y),'b')
        plt.show()