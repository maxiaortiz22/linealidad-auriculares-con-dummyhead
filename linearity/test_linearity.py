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

def linearity_tone_test(tone_type, chanel, buffer, sr):
    freqs = [125, 250, 500, 750, 1000, 1500, 2000, 3000, 4000, 6000, 8000]
    gains = [0, -5, -10, -15, -20, -25, -30, -35, -40, -45, -50]
    comp = [30.5, 18, 11, 6,  5.5, 5.5, 4.5, 2.5, 9.5, 17, 17.5]

    audio = np.array([])
    cal = []
    for i, frec in enumerate(freqs):
        for gain in gains:
            tono = np.array(tone(sr, frec, tone_type, gain, chanel, buffer))
            audio = np.append(audio, tono)

            cal_data = np.array(tone(sr, frec, tone_type, gain, chanel, buffer))
            rms_1Pa = RMS_cal(cal_data, nivel_dBHL=50, comp=comp[i])
            cal.append(rms_1Pa)
    
    return audio, cal


if __name__ == '__main__':
    from linearity import linealidad
    # Defino los parámetros:
    sr = 48000 # Frecuencia de sampleo [Hz]
    frec = 1000 # Frecuencia [Hz]
    tone_type = tone_generator.LINEARITY_TEST # Tipo de tono
    gain = 0 # Ganancia en dBFs
    chanel = 0x4 # Canal izquierdo = 0x4, Canal derecho = 0x5
    audio_seconds = 2 #Segundos de audio que quiero
    buffer = int(sr*audio_seconds*2) #(frecuencia de sampleo)*(segundos de audio)*(canales)

    #Genero el test:
    data, cal = linearity_tone_test(tone_type, chanel, buffer, sr)

    result = linealidad(cal, data, sr, auricular="Circumaural (ej: JBL750)")
