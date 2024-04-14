import time
import math
from pathlib import Path
from faster_whisper import WhisperModel
from pathlib import Path
from googletrans import Translator
from gtts import gTTS
import ffmpeg
from scipy.io import wavfile
#from dotenv import load_dotenv
import os
#load_dotenv()

translator = Translator()

input_video = '68.mp4'
input_video_name, file_ext = os.path.splitext(input_video)
source_location = 'source/video/'
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

def clean_audio():
    audio = f"audio-{input_video_name}.wav"
    stream = ffmpeg.input(audio)
    stream = ffmpeg.output(stream, f"clean-audio-{input_video_name}.wav")
    ffmpeg.run(stream, overwrite_output=True)
    #-af "highpass=f=300,asendcmd=0.0 afftdn sn start,asendcmd=1.5 afftdn sn stop,afftdn=nf=-20,dialoguenhance,lowpass=f=3000"

def extract_audio():
    extracted_audio = f"audio-{input_video_name}.wav"
    stream = ffmpeg.input(input_video)
    stream = ffmpeg.output(stream, extracted_audio)
    ffmpeg.run(stream, overwrite_output=True)

def transcribe(audio):
    model = WhisperModel('medium')
    segments, info = model.transcribe(audio, beam_size=5, initial_prompt=prompt)
    language = info[0]
    print("Transcription Language ", info[0], info.language_probability)
    segments = list(segments)
    f = open(f'transcribed-{input_video_name}.txt', 'w')
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
    t = open(f"translated-{input_video_name}.txt", "a")
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
    tts.save(f"translated-audio-{input_video_name}.wav")


def add_translated_audio_to_video():
    # remove original audio
    stream = ffmpeg.input("output-68.mp4", an=None)
    # add translated audio
    trans_audio = ffmpeg.input("translated-audio-68.wav")
    stream = ffmpeg.output(stream, trans_audio, "final-68.mp4")
    ffmpeg.run(stream, overwrite_output=True)

def run():
    extract_audio()
    clean_audio()
    source_audio = f"clean-audio-{input_video_name}.wav"
    language, segments = transcribe(source_audio)
    subtitle_file = generate_subtitle_file(
        translated=True, language=language, segments=segments)
    
    add_subtitle_to_video(
        soft_subtitle=True,
        subtitle_file=subtitle_file,
        subtitle_language=language
    )
    text_to_speech(f"translated-{input_video_name}.txt", 'en')
    add_translated_audio_to_video()

run()
