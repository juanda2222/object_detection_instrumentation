import serial, time

s = serial.Serial('COM4', 9600)
time.sleep(2)
String = s.readline()
print(String)
s.close()