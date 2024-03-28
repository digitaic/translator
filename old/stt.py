# speech recognition and returns text  Speech To Text

import speech_recognition as sr

r = sr.Recognizer()

# recorrer lista de archivos
# retornar textos
# espacios blancos?

with sr.AudioFile('source/audio3-spa.wav') as source:

    audio_text = r.listen(source)

    try:
        text = r.recognize_google(audio_text, language = 'es-ES')
        print('Converting audio transcripts into text ....')
        print(text)
        f = open('result/stt-spa.txt', 'w')
        f.write(text)
        

    except:
        print('Sorry.. run again...')

        
# https://towardsdatascience.com/easy-speech-to-text-with-python-3df0d973b426


