"""
La idea es abrir el micrófono y captar en 16 bits hasta que supero un treshold de silencio. Una vez detectado
que no hay silencio, corto ese stream y arranco otro a 24 bits con la duración de la prueba en cuestión. La razón
por la cual lo hago así es porque es intuitivo para mi realizar el treshold a 16 bits y no a 24. En el futuro
preguntarle a mati si sabe ajustar el treshold en 24.0

Saco lo de silencio de GrabarAudioRecortarSilencio.py y la grabación a 24 bits de:
https://stackoverflow.com/questions/23370556/recording-24-bit-audio-with-pyaudio

Al final tengo que usar 32bit float y no 24 así que tuve que mudarme a sounddevice para grabar y a librosa
para guardar el audio!!!
"""

from sys import byteorder
from array import array
import numpy as np
from scipy.signal import sosfilt
import os

import pyaudio
import sounddevice as sd
from scipy.io.wavfile import write

#Detector de sonido en 16 bits:
THRESHOLD = 5#30 #500 el original
CHUNK_SIZE_silence = 1024
FORMAT_silence = pyaudio.paInt16
RATE_silence = 44100

#Grabación en 32 bits flotantes:
CHANNELS = 1
RATE = 44100

THRESHOLD = THRESHOLD / 32767 #Divido por el máximo 16-bit value
sos = np.load(f"linearity/sos.npy")

def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD


def record(RECORD_SECONDS, sr=44100):
    """
    Detect when a signal appears and start recording
    """

    while 1:
        silenceRecording = sd.rec(CHUNK_SIZE_silence, samplerate=RATE_silence,
                     channels=CHANNELS, blocking=True, dtype='float32')
        #sd.wait()
        # little endian, signed short
        audio = sosfilt(sos, silenceRecording)
        #audio = audio/np.max(np.abs(audio))
        silent = is_silent(audio)

        if silent == False:
            break #Mato el loop cuando paso el umbral

    print('Señal detectada! Comienza grabación')

    myrecording = sd.rec(int(RECORD_SECONDS * sr), samplerate=sr,
                     channels=CHANNELS, blocking=True, dtype='float32')
    #sd.wait()

    #write('test_JBL750.wav', RATE, myrecording)
    return myrecording, sr


"""
if __name__ == '__main__':
    print("Envíar sonido")
    record()
    print(f"Listo, resultado escrito en {WAVE_OUTPUT_FILENAME}")
"""
