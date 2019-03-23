serial = [2,'z',10,5,0.03,0.1,0.4,0.1,0.04,1]
Vref = 5
def get_data(serial,Vref):
    serial_get = {'head' : serial[0],
        'selec' : serial[1],
        'gain' : serial[2],
        'n_data' : serial[3],
        'data': serial[4:len(serial)-1],
        'CR' : serial[len(serial)-1]
    }

    if serial_get.get('head') == 2:

        if serial_get.get('selec') == 'x':
            list_T1R1 = [s*Vref/serial_get.get('gain') for s in serial_get.get('data')]
            list_T1R2 = 0
            list_T2R1 = 0
            list_T2R2 = 0
            if  serial_get.get('CR') == 1:
                return list_T1R1, list_T1R2, list_T2R1, list_T2R2
        elif serial_get.get('selec') == 'y':
            list_T1R2 = [s*Vref/serial_get.get('gain') for s in serial_get.get('data')]
            list_T1R1 = 0
            list_T2R1 = 0
            list_T2R2 = 0
            if  serial_get.get('CR') == 1:
                return list_T1R1, list_T1R2, list_T2R1, list_T2R2
        elif serial_get.get('selec') == 'w':
            list_T2R1 = [s*Vref/serial_get.get('gain') for s in serial_get.get('data')]
            list_T1R2 = 0
            list_T1R1 = 0
            list_T2R2 = 0
            if  serial_get.get('CR') == 1:
                return list_T1R1, list_T1R2, list_T2R1, list_T2R2
        elif serial_get.get('selec') == 'z':
            list_T2R2 = [s*Vref/serial_get.get('gain') for s in serial_get.get('data')]
            list_T1R2 = 0
            list_T2R1 = 0
            list_T1R1 = 0 
            if  serial_get.get('CR') == 1:
                return list_T1R1, list_T1R2, list_T2R1, list_T2R2
                
a,b,c,d = get_data(serial,Vref)
print(a)
print(b)
print(c)
print(d)