import time
import math
from pathlib import Path
from faster_whisper import WhisperModel
from pathlib import Path
from googletrans import Translator
from gtts import gTTS
import ffmpeg
from scipy.io import wavfile
# from dotenv import load_dotenv
import os
# load_dotenv()

translator = Translator()

#input_video = input("Name of video file to process: ")
input_video = '68-raw.mp4'
input_video_name, file_ext = os.path.splitext(input_video)


def clean_audio():
    audio = f"audio-{input_video_name}.wav"
    stream = ffmpeg.input(audio).filter(audio, -af "highpass=f=300,asendcmd=0.0 afftdn sn start,asendcmd=1.5 afftdn sn stop,afftdn=nf=-20,dialoguenhance,lowpass=f=3000")
    stream = ffmpeg.output(stream, f"clean-audio-{input_video_name}.wav")
    ffmpeg.run(stream, overwrite_output=True)
    # iffmpeg -i <file> -af "highpass=f=300,asendcmd=0.0 afftdn sn start,asendcmd=1.5 afftdn sn stop,afftdn=nf=-20,dialoguenhance,lowpass=f=3000"
# https://superuser.com/questions/733061/reduce-background-noise-and-optimize-the-speech-from-an-audio-clip-using-ffmpeg

def extract_audio():
    extracted_audio = f"audio-{input_video_name}.wav"
    stream = ffmpeg.input(input_video)
    stream = ffmpeg.output(stream, extracted_audio)
    ffmpeg.run(stream, overwrite_output=True)



def run():
    extract_audio()
    clean_audio()

run()
