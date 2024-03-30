import time
import math
import ffmpeg

from faster_whisper import WhisperModel

input_video = 'source/video/hebrew_interview.mp4'
input_video_name = inpt_video.replace(".mp4", "")


source = 'source/audio/audio-spa.wav'
# source = 'source/audio/hebrew_interview.wav'
model = whisper.load_model('base')

result = model.transcribe(source, response_format='srt', fp16=False)
print(result["text"])

# f = open('result/text/hebrew_interview.srt', 'w+')
f = open('result/text/audio-spa.srt', 'w+')
f.write(str(result["text"]))
