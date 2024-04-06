from gtts import gTTS
import os

f = open('translated_text.txt')

tts = gTTS(f.read(), lang='en', tld='us')
tts.save('zaudio.mp3')