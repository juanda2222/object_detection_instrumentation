import numpy as np
import matplotlib.pyplot as plt
from get_data import get_data
from scipy.signal import butter, lfilter, freqz


class Temporal_extract(object):
    def __init__(self): #método
        print("_______temporal_extraction______")
 
    def resta(self,n,m):
        return n-m
 
    def temporal_extraction(self,y,Fs):
  
        
        print(y)
        dy = np.gradient(y) # derivate our input data

        max_index_vector = [] # to append the maximuns index

        # check if there is a sing change on each data pair
        for i in range(len(y)):
            checker = 0
            try:
                checker = np.sign(dy[i]) * np.sign(dy[i+1])
            except: # the last item in the vector
                break
                
            if int(checker) == -1: # its a maximun or a minimun
                print("¡cero found!")
                if dy[i] >= 0: # maximun
                    max_index_vector.append(i)
                    print ("max founded at index: " + str(i))
                else: # minimun
                    time_coef = i/Fs # time since the begining and the minimun
        
        
        if len(max_index_vector) >= 2: # founded atleast 2 maximuns
            time_coef = (max_index_vector[1] - max_index_vector[0]) / Fs # the time diference beween the two peaks
            print("more than 2")
        elif len(max_index_vector) > 0: # founded at least 1 maximun
            time_coef = max_index_vector[0] / Fs # time since the begining to the maximun
            print("just one: ")
        else:# no maximun nor minimun
            print("none")
            time_coef =  0 

        print(max_index_vector)
        print(format(time_coef, '.12g'))
        return time_coef * 1000
        
        """
        # Plot the filter bode diagram.
        w, h = freqz(b, a, worN=8000)
        plt.subplot(2, 1, 1)
        plt.plot(0.5 * Fs * w/ np.pi, np.abs(h), 'b')
        plt.plot(cutoff, 0.5 * np.sqrt(2), 'ko')
        plt.axvline(cutoff, color='k')
        plt.xlim(0, 0.5 * Fs)
        plt.title("Lowpass Filter Frequency Response")
        plt.xlabel('Frequency [Hz]')
        plt.grid()
        
        # plotting for debugging 
        length = len(y)
        T = 1/Fs
        fig, ax = plt.subplots()
        t  = np.linspace(0, length*T, length, endpoint = False) # now is a vector
        ax.plot(t, filter_y, '.') # "g" "b"
        ax.plot(t, filter_dy, 'o') # "g" "b"
        ax.plot(t, mult_filter_dy, "b") # "g" "b"
        plt.show()
        """
        
        
        """
        # misma historia con este codigo, no se puede leer 
        resta = self.resta
        dat = [abs(a) for a in y] 
        max_valor = max(dat)
        valor_min_dat = (max_valor)/4
        valores_max = []
        index_valores_max = []
        v = 0
        for i in dat:
            if i > valor_min_dat:
                valores_max.append(i)
                index_valores_max.append(v)
            v += 1            
        vector_dt = [1/Fs*m for m in index_valores_max.copy()]
        index_valores_max.append(0)
        index_valores_max = [1/Fs*a for a in index_valores_max]
        vector_dt.insert(0,0)
        vector_dt = list(map(resta,index_valores_max,vector_dt))
        vector_dt = vector_dt[1:len(vector_dt)-1]
        dT = sum(vector_dt)/len(vector_dt)
        return dT
        #print("Los máximos valores son: ",valores_max)
        #print("El tiempo de cada pico es: ", index_valores_max[0:len(index_valores_max)-1])
        #print("La diferencia entre cada tiempo es: ",vector_dt)
        #print("dT: ",dT)
        """

    def temporal_graphic(self,y,Fs):
        a = 1
        N = len(y)
        xt = np.linspace(0.0, N/(a*Fs), N//a)
        plt.cla()
        plt.plot(xt, y[0:N//a],'k')
        plt.show()


def get_butter_lowpass_coef(cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = get_butter_lowpass_coef(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

if __name__== "__main__":

    frec_muestreo = 8928
    sine_freq = 60
    num_datos = 50
    n = np.arange(num_datos)
    t = n * (1/frec_muestreo)
    s1 = np.sin(2 * np.pi * sine_freq * t) + (np.random.rand(num_datos))*0.05

    # use the extractor
    tc = Temporal_extract().temporal_extraction(s1, frec_muestreo)
    print(tc)