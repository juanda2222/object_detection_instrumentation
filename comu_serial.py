def get_serial_data():
    import serial
    s = serial.Serial('COM6', baudrate=9600)
    N = 35
    data_str = []
    i = 0
    while i <= N :
        data = s.readline()
        data_str.append(data.decode('utf-8')) 
        if i == N:
            break
        i += 1
    data_str = [x.rstrip() for x in data_str]        
    data_int = list(map(int,data_str))
    return data_int