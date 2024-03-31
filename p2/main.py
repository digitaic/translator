# googletrans==3.1.0a0
from googletrans import Translator 

import speech_recognition as sr

from gtts import gTTS
import os

translator = Translator()

source = open('source/text/ts-1.txt')
source = source.read()
dest_lan = 'en'

def detect_input_language(text):
    input_lan = translator.detect(str(text))
    print(input_lan)
    return input_lan
def translate(text, dest_lan):
    t = translator.translate(text, src= 'he', dest=dest_lan)
    #print(str(t))
    f = open('res.txt', 'w')
    f.write(str(t.text))


def run():
    detect_input_language(source)
    translate(str(source), dest_lan)

run()