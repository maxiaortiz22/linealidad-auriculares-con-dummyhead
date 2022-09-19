//ToneGenerator class:

#ifndef TONEGENERATOR_H
#define TONEGENERATOR_H


class ToneGenerator {
    int frequency, sampleRate;
    float angle = 0.0, offset = 0.0, amplitude;
    float* data;

public:

    ToneGenerator(int freq, float amp, int sr); //Constructor
    float getSample();
    void generateContinuousTone(float* data, int buffer_size);
    void tone_generator_free();

};

#endif
