import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import sosfilt, butter

#Filtros scipy:
def butter_bandpass_filter(data, lowcut, highcut, fs, order):
    sos = butter(order, [lowcut, highcut], fs=fs, btype='bandpass', output='sos')
    y = sosfilt(sos, data)
    return y

def butter_lowpass_filter(data, cutoff, fs, order):
    sos = butter(order, cutoff, fs=fs, btype='lowpass', output='sos')
    y = sosfilt(sos, data)
    return y


def butter_highpass_filter(data, cutoff, fs, order):
    sos = butter(order, cutoff, fs=fs, btype='highpass', output='sos')
    y = sosfilt(sos, data)
    return y

fc = 1000
fs = 44100
order = 2

lowcut = fc/(2**(1/6)) #Frecuencia de corte inferior bandas de tercio de octava
highcut = fc*(2**(1/6)) #Frecuencia de corte  superior bandas de tercio de octava

sos = butter_bandpass_filter(lowcut, highcut, fs, order)

seconds = 256/fs
f = 1000

t = np.arange(0, seconds, 1/fs, dtype='float32')
x = np.cos(2*np.pi*f*t).astype('float32')

filtered_audio = sosfilt(sos, x)

plt.plot(x)
plt.plot(filtered_audio)

plt.show()