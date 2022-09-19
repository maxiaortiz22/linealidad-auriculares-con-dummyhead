#define _USE_MATH_DEFINES
#include <cmath>
#include "tone_generator.h"

//Define the implementations of the ToneGenerator class:
ToneGenerator::ToneGenerator(int freq, float amp, int sr) : frequency(freq), amplitude(amp), sampleRate(sr) {
    offset = 2 * M_PI * (float) frequency / (float) sampleRate;
}

float ToneGenerator::getSample() {
    float sample = amplitude * sin(angle);
    angle += offset;
    return sample;
}

//Generating the tone:
void ToneGenerator::generateContinuousTone(float* data, int buffer_size){
    //main working loop:
    for (int i = 0; i < buffer_size; i += 1) {
        float sample = ToneGenerator::getSample();
        data[i] = sample;
    }
}

void ToneGenerator::tone_generator_free() {
    if (data == NULL) {
        return;
    }
    free(data);
    data = NULL;
}