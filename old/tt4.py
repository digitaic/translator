from gtts import gTTS
import os
import speech_recognition as sr

def readText(url):
    f = open(url, 'r')
    print(f.read)
    return f.read()

def text_to_speech(url):
    text = readText(url)
    print(text)
    tts = gTTS(text)
    tts.save('result/audio/result4.mp3')
    os.system('start result/audio/result4.mp3')

def main():
    text_to_speech('result/translated-text.txt')

readText('result/translated-text.txt')