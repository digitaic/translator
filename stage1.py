# https://campus.datacamp.com/courses/spoken-language-processing-in-python/using-the-python-speechrecognition-library?ex=5
# speechRecognition
# https://medium.com/wiki-flood/python-project-convert-speech-to-text-and-text-to-speech-8065972e5e58
# https://medium.com/@jianchang512/developing-a-video-translation-and-dubbing-tool-using-python-a1120b8b5b47

# Noise reduction
from scipy.io import wavfile
import numpy as np
import noisereduce as nr

rate, data = wavfile.read('source/audio-spa.wav')

reduced_noise = nr.reduce_noise(y=data, sr= rate)
wavfile.write("result/audio/audio-spa-clean.wav", rate, reduced_noise)