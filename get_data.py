from comu_serial import get_serial_data
#serial = [2,'z',10,5,0.03,0.1,0.4,0.1,0.04,1]
def get_data():
    serial = get_serial_data()
    Vref = 5
    serial_get = {'head' : serial[0],
        'selec' : serial[1],
        'gain' : serial[2],
        'n_data' : serial[3],
        'data': serial[4:len(serial)-1],
        'CR' : serial[len(serial)-1]
    }
    if serial_get.get('head') == 2:

        if serial_get.get('selec') == 0: # cuando la opcione es x
            list_T1R1 = [s*Vref/serial_get.get('gain') for s in serial_get.get('data')]
            list_T1R2 = 0
            list_T2R1 = 0
            list_T2R2 = 0
            if  serial_get.get('CR') == 1:  
                return list_T1R1, list_T1R2, list_T2R1, list_T2R2
        elif serial_get.get('selec') == 1: # cuando la opcione es y
            list_T1R2 = [s*Vref/serial_get.get('gain') for s in serial_get.get('data')]
            list_T1R1 = 0
            list_T2R1 = 0
            list_T2R2 = 0
            if  serial_get.get('CR') == 1:
                return list_T1R1, list_T1R2, list_T2R1, list_T2R2
        elif serial_get.get('selec') == 2: # cuando la opcione es w
            list_T2R1 = [s*Vref/serial_get.get('gain') for s in serial_get.get('data')]
            list_T1R2 = 0
            list_T1R1 = 0
            list_T2R2 = 0
            if  serial_get.get('CR') == 1:
                return list_T1R1, list_T1R2, list_T2R1, list_T2R2
        elif serial_get.get('selec') == 3: # cuando la opcione es z
            list_T2R2 = [s*Vref/serial_get.get('gain') for s in serial_get.get('data')]
            list_T1R2 = 0
            list_T2R1 = 0
            list_T1R1 = 0 
            if  serial_get.get('CR') == 1:
                return list_T1R1, list_T1R2, list_T2R1, list_T2R2
    else:
        print("No se encuentra el head")
        list_T2R2 = 0
        list_T1R2 = 0
        list_T2R1 = 0
        list_T1R1 = 0
        return list_T1R1, list_T1R2, list_T2R1, list_T2R2            
list_T1R1, list_T1R2, list_T2R1, list_T2R2 = get_data()
print(list_T1R1)
print(list_T1R2)
print(list_T2R1)
print(list_T2R2)