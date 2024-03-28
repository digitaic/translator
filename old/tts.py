import pyttsx3
# https://thepythoncode.com/article/convert-text-to-speech-in-python

# voices , cloning, ai
# https://github.com/suno-ai/bark
# https://www.youtube.com/watch?v=rU5Do9yHbwM
# tacotron2


engine = pyttsx3.init()

t = open('result/translated-text.txt', 'r')

ttr = t.read()
voices = engine.getProperty('voices')
# print(voices)
engine.setProperty('rate', 125)
engine.setProperty('voice', voices[1].id)
# engine.say(ttr)
engine.save_to_file(ttr, 'result/audio/translated.mp3')
engine.runAndWait()
