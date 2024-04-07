import time
import math
import ffmpeg
from faster_whisper import WhisperModel
from pathlib import Path
from googletrans import Translator
from gtts import gTTS
from ffmpeg import FFmpeg
#from dotenv import load_dotenv
#from bark import SAMPLE_RATE, generate_audio, preload_models
#from scipy.io.wavfile import write as write_wav
#from IPython.display import Audio
#import nltk
#import numpy as np
import os

#load_dotenv()

translator = Translator()
#preload_models()
text_prompt = """
     Hello, my name is Suno. And, uh — and I like pizza. [laughs] 
     But I also have other interests such as playing tic tac toe.
"""
#audio_array = generate_audio(text.read())

# save audio to disk
#write_wav("bark_generation.wav", SAMPLE_RATE, audio_array)
  
# play text in notebook
#Audio(audio_array, rate=SAMPLE_RATE)

#openaiAK = os.environ["OPENAI_API_KEY"]

source_location = 'source/video/'
# input_video = 'clase-15.mp4'
input_video = '68.mp4'
# input_video = 'he.mp4'
# input_video = 'audio-spa.wav'
# input_video_name = input_video.replace(".mp4", "")
input_video_name = input_video.replace(".mp4", "")
extracted_audio_location = 'process/audio/'
out_lan = 'en'


prompt = (
    f"This is a podcast audio file that teaches how to use Microsoft Power BI."
    f"It's language is hihly technical,  statistical language,  data language."
    f"Teacher is Sonia a female whose native language is spanish from Latin America.  Her talk is highly technical."
    f"This file will be transcribed and translated to multiple languages"
    f"Teacher uses statistical language,  average, mode, mean, max, and many more statistical words and concepts."
    f"Teacher uses a dataset Athletes Events contains data of Olympic events from 1896 to 2016."
    f"It contains data about year of event, country, delegations, athletes ages, athletes height, weight, Body Mass Index BMI."
    f"It contains the list of medals earned by each delegation."
)

def clean_audio(audio):
    stream = ffmpeg.input("audio-spa.wav")
    stream = ffmpeg.output(
            "clean_audio_spa.wav",
            vf = "highpass=f=199, lowpass=f=3000",
        )
    ffmpeg.run(stream)
    #return clean

def extract_audio():
    extracted_audio = f"audio-{input_video_name}.wav"
    stream = ffmpeg.input(input_video)
    # stream = ffmpeg.output(stream, f"{extracted_audio_location}{extracted_audio}")
    stream = ffmpeg.output(stream, f"{extracted_audio}")
    ffmpeg.run(stream, overwrite_output=True)
    return extracted_audio


def transcribe(audio):
    model = WhisperModel('medium')
    segments, info = model.transcribe(audio, beam_size=5, initial_prompt=prompt)
    language = info[0]
    print("Transcription Language ", info[0], info.language_probability)
    segments = list(segments)
    f = open('transcribed_text.txt', 'w')
    for segment in segments:
        # print(segment)
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, translate_text(segment.text, 'es', 'en')))
        f.write(str(segment.text))
    return language, segments


def translate_text(text, input_lan, out_lan):
    return translator.translate(text, src=input_lan, dest=out_lan).text

def format_time(seconds):
    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:01d},{milliseconds:03d}"
    return formatted_time


def generate_subtitle_file(translated, language, segments):
    t = open('translated_text.txt', 'a')
    subtitle_file = f"sub-{input_video_name}.{language}.srt"
    text = ""
    text_to_read = ""

    if translated:
        for index, segment in enumerate(segments):
            segment_start = format_time(segment.start)
            segment_end = format_time(segment.end)
            text += f"{str(index+1)} \n"
            text += f"{segment_start} --> {segment_end} \n"
            text += f"{translate_text(segment.text, language, out_lan)} \n"
            text += "\n"
            text_to_read += f"{translate_text(segment.text, language, out_lan)} \n"
            text_to_read += "\n"
    else:
        for index, segment in enumerate(segments):
            segment_start = format_time(segment.start)
            segment_end = format_time(segment.end)
            text += f"{str(index+1)} \n"
            text += f"{segment_start} --> {segment_end} \n"
            text += f"{segment.text} \n"
            text += "\n"

    f = open(subtitle_file, "w")
    f.write(text)
    f.close()
    t.write(text_to_read)
    t.close()

    return subtitle_file


def add_subtitle_to_video(soft_subtitle, subtitle_file, subtitle_language):

    video_input_stream = ffmpeg.input(input_video)
    subtitle_input_stream = ffmpeg.input(subtitle_file)
    output_video = f"output-{input_video_name}.mp4"
    subtitle_track_title = subtitle_file.replace(".srt", "")

    if soft_subtitle:
        stream = ffmpeg.output(
            video_input_stream, subtitle_input_stream, output_video, **{"c": "copy", "c:s": "mov_text"},
            **{"metadata:s:s:0": f"language={subtitle_language}",
               "metadata:s:s:0": f"title={subtitle_track_title}"}
        )
        ffmpeg.run(stream, overwrite_output=True)
    else:
        stream = ffmpeg.output(video_input_stream, output_video,
                               vf=f"subtitles={subtitle_file}")
        ffmpeg.run(stream, overwrite_output=True)

def read_text(file):
    f = open(file, 'r')
    return str(f.read())


def text_to_speech(text, language):
    f = open(text)
    tts = gTTS(f.read(), lang='en', tld='us')
    tts.save('p1.mp3')


def run():
    extracted_audio = extract_audio()
    clean_audio(extracted_audio)
    """
    language, segments = transcribe(extracted_audio)
    subtitle_file = generate_subtitle_file(
        translated=True, language=language, segments=segments)
    
    add_subtitle_to_video(
        soft_subtitle=True,
        subtitle_file=subtitle_file,
        subtitle_language=language
    )
    text_to_speech("translated_text.txt", 'en')
    """

run()
