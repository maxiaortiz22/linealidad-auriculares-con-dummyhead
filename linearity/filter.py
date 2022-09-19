from scipy.signal import butter
import numpy as np

#Filtros scipy:
def butter_bandpass_filter(lowcut, highcut, fs, order):
    sos = butter(order, [lowcut, highcut], fs=fs, btype='bandpass', output='sos')
    #y = sosfilt(sos, data)
    return sos



def bandpass_filtered_signals(data, fs, order, type='octave band'):
    filtered_signal = butter_bandpass_filter(data, lowcut, highcut, fs, order) # Filtro la señal


if __name__ == '__main__':

    fc = 10000
    fs = 44100
    order = 6
    
    lowcut = fc/(2**(1/6)) #Frecuencia de corte inferior bandas de tercio de octava
    highcut = fc*(2**(1/6)) #Frecuencia de corte  superior bandas de tercio de octava

    sos = butter_bandpass_filter(lowcut, highcut, fs, order)

    np.save("sos.npy", sos)