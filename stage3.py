# https://medium.com/rasa-blog/how-to-build-a-voice-assistant-with-open-source-rasa-and-mozilla-tools-c05c4ec698c6
# https://medium.com/@jianchang512/developing-a-video-translation-and-dubbing-tool-using-python-a1120b8b5b47

# **   https://medium.com/@jianchang512/developing-a-video-translation-and-dubbing-tool-using-python-a1120b8b5b47

# **** https://www.nickersonj.com/posts/whisper-and-tortoise/

 # stage 1: tranlate a given audio.  
#   generate text file
# issue: does not translate all audio: 
# test other stt (transcription) apis: googletrans,  ???

import whisper
#from openai import OpenAI

print('... stage 1')

model = whisper.load_model("base")
source = 'source/audio-spa.wav'

def translateAudio(audio_source):
    audio = whisper.load_audio(audio_source)
    
    
    
    #options = whisper.DecodingOptions(task = 'translate', language='es' )
    #result = whisper.decode(model, mel, options)
    #result = whisper.transcribe(audio, fp16=False)
    result = model.transcribe(audio, fp16=False)

    #print(result.text)
    print(result["text"])

    f = open('result/text/translated-audio.txt', 'w+')
    #f.write(str(result.text))
    f.write(str(result["text"]))

translateAudio(source)