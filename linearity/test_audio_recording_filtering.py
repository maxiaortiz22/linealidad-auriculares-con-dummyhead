# Agrego el path donde está el tone_generator al archivo:
from cProfile import label
import sounddevice as sd
import numpy as np
from scipy.signal import sosfilt, butter

#Filtros scipy:
def butter_bandpass_filter(lowcut, highcut, fs, order):
    sos = butter(order, [lowcut, highcut], fs=fs, btype='bandpass', output='sos')
    #y = sosfilt(sos, data)
    return sos

def butter_lowpass_filter(data, cutoff, fs, order):
    sos = butter(order, cutoff, fs=fs, btype='lowpass', output='sos')
    y = sosfilt(sos, data)
    return y


def butter_highpass_filter(data, cutoff, fs, order):
    sos = butter(order, cutoff, fs=fs, btype='highpass', output='sos')
    y = sosfilt(sos, data)
    return y

fc = 16000
fs = 44100
order = 1

lowcut = fc/(2**(1/6)) #Frecuencia de corte inferior bandas de tercio de octava
highcut = fc*(2**(1/6)) #Frecuencia de corte  superior bandas de tercio de octava

sos = butter_bandpass_filter(lowcut, highcut, fs, order)

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    
    # Defino los parámetros:
    sr = 44100 # Frecuencia de sampleo [Hz]
    buffer = 512

    #Genero el test:
    data = sd.rec(buffer, samplerate=sr, channels=1, blocking=True, dtype='float32')
    sd.wait()
    
    print(np.max(data))

    #sos = np.load(f"sos.npy")
    filtered_data = sosfilt(sos, data)
    filtered_low = butter_lowpass_filter(data, highcut, fs, order)
    filtered_high = butter_highpass_filter(data, lowcut, fs, order)

    print(np.max(filtered_data))

    plt.plot(data, label='Original')
    plt.plot(filtered_data, label='pasabanda')
    #plt.plot(filtered_low, label='pasabajos')
    plt.plot(filtered_high, label='pasaaltos')
    plt.legend()
    plt.show()
