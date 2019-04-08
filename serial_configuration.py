from comu_serial import setup_serial_data

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

#sample, resolution, Vref, CR = serial_configuration()
#print(sample)
#print(resolution)
#print(Vref)
#print(CR)