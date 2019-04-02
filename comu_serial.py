import serial

def setup_serial_data():
    s = serial.Serial('COM6', baudrate=9600) 
    N = 4
    data_str = []
    i = 0
    while i <= N :
        data = s.readline()
        data_str.append(data.decode('utf-8')) 
        if i == N:
            break
        i += 1
    data_str = [x.rstrip() for x in data_str]        
    data_setup = list(map(int,data_str))
    ##s.close()
    return data_setup
    #print(data_setup)

def get_serial_data():
    s = serial.Serial('COM6', baudrate=9600) 
    N = 185
    M = 4*N+28
    data_str = []
    i = 0
    while i <= M :
        data = s.readline()
        data_str.append(data.decode('utf-8')) 
        if i == M:
            break
        i += 1
    data_str = [x.rstrip() for x in data_str]        
    data_int = list(map(int,data_str))
    return data_int
    #print(data_int)
    #print(len(data_int))
#get_serial_data()
#setup_serial_data()