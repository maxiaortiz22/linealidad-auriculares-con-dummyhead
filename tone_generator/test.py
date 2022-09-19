import tone_generator
import sounddevice as sd
import numpy as np
import soundfile as sf

SR = 48000 #Sample rate
AMP = 1 #Amplitude
FREQ_1 = 1000 #Frequency
FREQ_2 = 1003 #Frequency
SECONDS = 2

total_samples = SECONDS*SR
buffer = 256

tone = tone_generator.ToneGenerator(FREQ_1, AMP, SR) #Instancio la clase

audio = []
for i in range(int(total_samples/buffer)):
    data = tone.generateContinuousTone(buffer)

    audio.extend(data)

sd.play(audio, SR)
sd.wait()

sf.write('test.wav', audio, SR)

tone.tone_generator_free()