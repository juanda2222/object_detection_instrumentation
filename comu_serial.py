import time
import serial
import numpy as np
N = 35
data = np.zeros((N, 1))
# Abrimos la conexión con Arduino
s = serial.Serial('COM6', baudrate=9600, timeout=1.0)
with s:
    ii = 0
    while ii < N:
        try:
            line = s.readline()
            if not line:
                continue
            data[ii] = np.fromstring(line.decode('ascii', errors='replace'),sep=',')            
            ii += 1
            print(data[ii])
        except KeyboardInterrupt:
            print("Exiting")
            break
