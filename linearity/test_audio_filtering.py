# Agrego el path donde está el tone_generator al archivo:
import sys
sys.path.append(r'C:\Users\maxia\OneDrive\Desktop\uSound\Código del audiómetro\audiometro-uSound\python-swig')
import tone_generator
from linearity import RMS_cal
import numpy as np

def tone(sr, frec, tone_type, gain, chanel, buffer):

    tone_generator.tone_generator_free()

    tone_generator.tone_generator_alloc(sr)
    tone_generator.tone_generator_setValue(0x0, 0) #Saco el bypass!
    tone_generator.tone_generator_setValue(0x1, frec) #Frecuencia en [Hz]
    tone_generator.tone_generator_setValue(0x9, tone_type) #Tipo de tono
    tone_generator.tone_generator_setValue(0x2, gain) #Ganancia en dBFS
    tone_generator.tone_generator_setValue(0x3, chanel) #Canal de emisión

    data = tone_generator.tone_generator_interval_process(buffer)
    data = data.tolist()

    # Me quedo solo con el canal elegido y elimino los 0:
    tono = []
    if chanel == 0x4: #Canal izquierdo
        for i in range(0, len(data), 2):
            tono.append(data[i])
    elif chanel == 0x5: #Canal derecho
        for i in range(1, len(data), 2):
            tono.append(data[i])

    tone_generator.tone_generator_free()

    return tono


if __name__ == '__main__':
    from scipy.signal import sosfilt

    # Defino los parámetros:
    sr = 44100 # Frecuencia de sampleo [Hz]
    frec = 1000 # Frecuencia [Hz]
    tone_type = tone_generator.CONTINUOUS_TONE # Tipo de tono
    gain = 0 # Ganancia en dBFs
    chanel = 0x4 # Canal izquierdo = 0x4, Canal derecho = 0x5
    audio_seconds = 2 #Segundos de audio que quiero
    buffer = 256#int(sr*audio_seconds*2) #(frecuencia de sampleo)*(segundos de audio)*(canales)

    #Genero el test:
    data = tone(sr, frec, tone_type, gain, chanel, buffer)
    
    print(np.max(data))

    sos = np.load(f"sos.npy")
    filtered_data = sosfilt(sos, data)

    print(np.max(filtered_data))
