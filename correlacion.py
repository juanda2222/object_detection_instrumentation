import numpy
from scipy import signal
import time

input_signal = [1,3,5,3,8]
signal_corr = numpy.correlate(input_signal, input_signal, mode='valid')

for i in range(8):
    b = [i-2,i,5,3,8]
    corr1 = signal.fftconvolve(b, input_signal[::-1], mode='valid') 
    corr = numpy.correlate(input_signal, b, mode='valid')
    print(corr)
    if signal_corr == corr:
        print("La señal es igual")
    time.sleep(1)