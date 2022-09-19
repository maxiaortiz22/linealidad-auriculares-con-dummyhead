#import os

#os.system("swig -c++ -python tone_generator_wrapper.i")
#os.system("""g++ -fpic -c Tone_generator/generator.h 
#                           Tone_generator/tone_generator.h
#                           tone_generator_wrapper_wrap.cxx 
#                           Tone_generator/tone_generator.cpp 
#                           -I/Users/maxia/anaconda3/include/python3.9.7""")

#os.system('gcc -shared tone_generator_wrapper_wrap.cxx -o _tone_generator.so -lstdc++')

from distutils.core import setup, Extension
import numpy

#Genero el wrapper:
name = "tone_generator"      # name of the module
version = "1.0"  # the module's version number

setup(name=name, version=version,
      ext_modules=[Extension(name='_tone_generator', 
      # SWIG requires an underscore as a prefix for the module name
             sources=["tone_generator_wrapper.i", "Tone_generator/tone_generator.cpp"],# "usoundlib_params.h"],
             include_dirs=[numpy.get_include(), "Tone generator"],
             swig_opts=["-c++"])
    ])



"""
# compile module
python setup.py build_ext 
# install in the current directory
python setup.py install --install-platlib=.
and test with:

python -c 'import hw'     # test module
"""