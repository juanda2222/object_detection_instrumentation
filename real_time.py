import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from scipy.fftpack import fft
N = 600
T = 1.0/100.0 
COUNT = 100
fig, (ax,ax1,ax2) = plt.subplots(3,1,sharex='all', sharey='all')
ax.set_ylim([-5, 5])
ax.set_xlim(0, COUNT)
ax1.set_ylim([-5, 5])
ax1.set_xlim(0, COUNT)
signal = {'y':[],'y1':[]}
SignalOut = {'y3':[]}
lines = [ax.plot([], [])[0] for _ in signal.items()]
lines1 = [ax1.plot([], [])[0] for _ in SignalOut.items()]
xdata = []
ydata = [] 
def next():
   i = 0
   while i <= COUNT:
      i += 1
      yield i
def update(i):
   x = np.linspace(0.0,N*T,N)
   xdata.append(i)
   y = np.cos(i*60*2*3.14) 
   #yf = fft(y)
   #print(len(y))
   #y = np.sin(i*50.0 * 2.0*np.pi*x) + 0.5*np.sin((380.0//i) * 2.0*np.pi*x)+ np.cos(120.0 * 2.0*np.pi*x)
   signal['y'] = y
   signal['y1'] = y/2
   
   SignalOut['y3'] = 3*y
   #ydata.append(y)
   for name, line in zip(SignalOut.keys(), lines1):
    _, ly = line.get_data()
    ly = np.append(ly, SignalOut[name])
    _xdata = np.arange(ly.size)
    line.set_data(_xdata, ly)
    SignalOut[name] = [] 
   #lines1.set_dataxf, 2.0/N * np.abs(yf[0:N//2]))  
   for name, line in zip(signal.keys(), lines):
        _, ly = line.get_data()
        ly = np.append(ly, signal[name])
        _xdata = np.arange(ly.size)
        line.set_data(_xdata, ly)
        signal[name] = [] 

   return lines,lines1

if __name__ == '__main__':
   a = animation.FuncAnimation(fig, update, next, blit = False, interval = 60,
                               repeat = False)
   
   plt.show()
   print(signal['y1'])
