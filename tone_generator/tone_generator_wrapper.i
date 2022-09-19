%module tone_generator

%{
#define SWIG_FILE_WITH_INIT
#include "Tone_generator/tone_generator.h"
%}

// Include the implementation with numpy
%include "numpy.i"

%init %{
    import_array();
%}

%apply (float* ARGOUT_ARRAY1, int DIM1) {(float* data, int buffer_size)}

%include "Tone_generator/tone_generator.h"

