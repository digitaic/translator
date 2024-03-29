import whisper

source = 'source/audio/audio-spa.wav'
#source = 'source/audio/hebrew_interview.wav'
model = whisper.load_model('base')

result = model.transcribe(source, response_format='srt', fp16=False)
print(result["text"])

#f = open('result/text/hebrew_interview.srt', 'w+')
f = open('result/text/audio-spa.srt', 'w+')
f.write(str(result["text"]))