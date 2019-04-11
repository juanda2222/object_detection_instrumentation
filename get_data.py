from comu_serial import get_serial_data
from comu_serial import setup_serial_data
#serial = [2,0,10,5,0.03,0.1,0.4,0.1,0.04,1]

def get_data():
    header = 1500   
    sample, resolution, Vref, CR = serial_configuration()
    serial = get_serial_data()
    serial = serial[5:len(serial)]

    index_head = [i for i, x in enumerate(serial) if x == header]
    index_header1 = index_head[0]    
    index_header2 = index_head[1]
    index_header3 = index_head[2]
    index_header4 = index_head[3]

    serial_get = {'selec1' : serial[index_header1+1], 'selec2' : serial[index_header2+1], 'selec3' : serial[index_header3+1],'selec4' : serial[index_header4+1], 
        'gain1' : serial[index_header1+2], 'gain2' : serial[index_header2+2], 'gain3' : serial[index_header3+2],'gain4' : serial[index_header4+2], 
        'n_data1' : serial[index_header1+3], 'n_data2' : serial[index_header2+3], 'n_data3' : serial[index_header3+3],'n_data4' : serial[index_header4+3], 
        'data1' : serial[index_header1+4:index_header2-1], 'data2' : serial[index_header2+4:index_header3-1], 'data3' : serial[index_header3+4:index_header4-1],'data4' : serial[index_header4+4:len(serial)-1], 
        'CR1' : serial[index_header2-1], 'CR2' : serial[index_header3-1], 'CR3' : serial[index_header4-1],'CR4' : serial[len(serial)-1],                 
    }        

    # initialize each vector as empty to avoid exception                  
    list_T1R1 = None
    list_T1R2 = None
    list_T2R1 = None
    list_T2R2 = None

    if serial_get.get('selec1') == 87: # cuando la opcione es x
        list_T1R1 = [s*Vref/resolution*serial_get.get('gain1') for s in serial_get.get('data1')]
        if  serial_get.get('CR1') == 1:              
            if serial_get.get('selec2') == 88: # cuando la opcione es y
                list_T1R2 = [s*Vref/resolution*serial_get.get('gain2') for s in serial_get.get('data2')]                
                if  serial_get.get('CR2') == 1:                    
                    if serial_get.get('selec3') == 89: # cuando la opcione es w
                        list_T2R1 = [s*Vref/resolution*serial_get.get('gain3') for s in serial_get.get('data3')]                        
                        if  serial_get.get('CR3') == 1:                           
                            if serial_get.get('selec4') == 90: # cuando la opcione es z
                                list_T2R2 = [s*Vref/resolution*serial_get.get('gain4') for s in serial_get.get('data4')]                                
                                if  serial_get.get('CR4') == 1:
                                    return list_T1R1, list_T1R2, list_T2R1, list_T2R2  
 

def serial_configuration():
    bytes_config = setup_serial_data()
    while bytes_config[0] != 1:        
        bytes_config = setup_serial_data()
        if bytes_config[0] == 1:
            break
    sample = bytes_config[1]
    resolution = bytes_config[2]
    Vref = bytes_config[3]
    CR = bytes_config[4]
    if CR == 1:
        return sample, resolution, Vref, CR

