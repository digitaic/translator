# https://www.digitalocean.com/community/tutorials/how-to-generate-and-add-subtitles-to-videos-using-python-openai-whisper-and-ffmpeg 

import time
import math
from pathlib import Path
import ffmpeg
from faster_whisper import WhisperModel
from googletrans import Translator
from scipy.io import wavfile
import pydub
from gtts import gTTS

import os

# translator = Translator(service_urls=['translate.googleapis.com'])
translator = Translator()

input_video = input("Name of video file to process: ")
input_video_name, file_ext = os.path.splitext(input_video)
source_location = 'source/video/'
extracted_audio_location = 'process/audio/'
out_lan = 'en'
model_size = "medium"

prompt = (
    f"This is a podcast audio file that teaches how to use Microsoft Power BI."
    f"It was created in native spanish from latin america."
    f"Uses technical langauge related to statistics and data science.  Common words are Average, Median, Mode, Standard Deviation."
    f"It's language is hihly technical,  statistical language,  data language."
    f"Teacher is Sonia a female whose native language is spanish from Latin America.  Her talk is highly technical."
    f"This file will be transcribed and translated to multiple languages"
    f"Teacher uses statistical language,  average, mode, mean, max, and many more statistical words and concepts."
    f"Teacher uses a dataset Athletes Events contains data of Olympic events from 1896 to 2016."
    f"It contains data about year of event, country, delegations, athletes ages, athletes height, weight, Body Mass Index BMI."
    f"It contains the list of medals earned by each delegation."
    f"Este es un podcast en lenguaje Español Latino que enseña o instruye sobre el uso de Microsoft PowerBI"
    f"El texto es tecnico.  Habla sore estadistica, datos, medidas, series de tiempo, calculos, columnas, filas, tablas."
    f"Usa un dataset o fuente de datos que contiene data de todas las Olimpiadas:  pais,  equipo, medallas, genero, edad.  Usa palabras como atleta, equipo, muestra, polacion, moda, promedio, average, desviacion estandar."
    f"common words: average x, sum x, "
)


def clean_audio():
    audio = f"audio-{input_video_name}.wav"
    stream = ffmpeg.input(audio)
    stream = ffmpeg.output(stream, f"clean-audio-{input_video_name}.wav")
    ffmpeg.run(stream, overwrite_output=True)
    # -af "highpass=f=300,asendcmd=0.0 afftdn sn start,asendcmd=1.5 afftdn sn stop,afftdn=nf=-20,dialoguenhance,lowpass=f=3000"


def extract_audio():
    # ffmpeg -i 1.mp4 -acodec pcm_s16le -f s16le -ac 1 -ar 16000 -f wav audio.wav
    extracted_audio = f"audio-{input_video_name}.wav"
    print("jea 57")
    try:
        input = ffmpeg.input(input_video)
        audio = input.audio
        audio = ffmpeg.output(audio, extracted_audio)
        ffmpeg.run(audio, overwrite_output=True)
        # .output('-', format='s16le', acodec='pcm_s16le', ac=1, ar='16k' )
        # **{'acodec:pcm'}
    except OSError as e:
        print(f"[Line 54] Error extracting audio from video: {e.stderr}.")
        return None


def split_audio():
    pydub.silence.detect_nonsilent(
        normalized_sound, min_silence_len=min_slient, silence_tresh=-20.0 - thd, seek_step=1)
    return 1


def transcribe_audio(audio):
    try:
        transcribed_words = ""
        transcribed_text = ""
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
        segments, info = model.transcribe(
            audio, beam_size=5, language="es", initial_prompt=prompt, word_timestamps=True
        )
        language = info[0]
        print("Transcription Language ", info[0], info.language_probability)
        segments = list(segments)
        for segment in segments:
            transcribed_text += f"{segment.text}\n\n"
            for word in segment.words:
                print("[%.2fs -> %.2fs] %s" %
                      (word.start, word.end, word.word)),
                transcribed_words += f"{word.word}\n"
        f = open(f'transcribed-{input_video_name}.txt', 'w')
        f.write(str(transcribed_text))
        f.close()
        w = open(f'transcribed-words-{input_video_name}.txt', 'w')
        w.write(str(transcribed_words))
        w.close()

        return language, segments
    except Exception as e:
        print(f"[Line 62] Error transcribing audio: {e}.")
        return None


def translate_text(text, input_lan, out_lan):
    try:
        return translator.translate(str(text), src=str(input_lan), dest=out_lan).text
    except Exception as e:
        print(f"[Line 87] Error translating text: {e}.")
        return None


def format_time(seconds):
    try:
        hours = math.floor(seconds / 3600)
        seconds %= 3600
        minutes = math.floor(seconds / 60)
        seconds %= 60
        milliseconds = round((seconds - math.floor(seconds)) * 1000)
        seconds = math.floor(seconds)
        formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:01d},{milliseconds:03d}"
        return formatted_time
    except Exception as e:
        print(f"[Line 94] Error time format: {e}.")
        return None


def generate_subtitle_file(translated, language, segments):
    trans_text = ""
    original_text = ""
    trans_text_to_read = ""
    text_to_read = ""
    duration = 0

    try:
        # if index < len(segments):
        trans_subtitle_file = f"sub-{input_video_name}-{out_lan}.srt"
        for index, segment in enumerate(segments, start=0):
            segment_start = format_time(segment.start)
            segment_end = format_time(segment.end)
            trans_text += f"{str(index+1)} \n"
            trans_text += f"{segment_start} --> {segment_end} \n"
            trans_text += f"{translate_text(segment.text, language, out_lan)} \n"
            trans_text += "\n"
            duration = segment.end - segment.start
            # trans_text_to_read += f"{segment_start} ---> {segment_end} duration: {duration:.2} \n"
            trans_text_to_read += f"{translate_text(segment.text, language, out_lan)} \n"
            trans_text_to_read += "\n"

        original_subtitle_file = f"sub-{input_video_name}-{language}.srt"
        for index, segment in enumerate(segments):
            segment_start = format_time(segment.start)
            segment_end = format_time(segment.end)
            original_text += f"{str(index+1)} \n"
            original_text += f"{segment_start} --> {segment_end} \n"
            original_text += f"{segment.text} \n"
            original_text += "\n"

        f = open(trans_subtitle_file, "w")
        f.write(trans_text)
        f.close()
        t = open(f"translated-{input_video_name}.txt", "w")
        t.write(trans_text_to_read)
        t.close()
        g = open(original_subtitle_file, "w")
        g.write(original_text)
        g.close()
    except Exception as e:
        print(f"[Line 149] Error generate subtitle file: {e}.")
        return None

    # return originl_subtitle_file, trans_subtitle_file


def add_subtitle_to_video(soft_subtitle, subtitle_file, subtitle_language):
    video_input_stream = ffmpeg.input(input_video)
    subtitle_input_stream = ffmpeg.input(subtitle_file)
    output_video = f"output-{input_video_name}.mp4"
    subtitle_track_title = subtitle_file.replace(".srt", "")

    try:
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
    except Exception as e:
        print(f"[Line 156] Error add subtitle to video: {e}.")
        return None


def force_alignment(text, audiuo):
    string = "task_language=es|is_text_type=subtitles|os_task_file_format=srt"
    return 1


def read_text(file):
    try:
        f = open(file, 'r')
        return str(f.read())
    except Exception as e:
        print(f"[Line 184] Error read text: {e}.")
        return None


def text_to_speech(text, language):
    try:
        f = open(text)
        tts = gTTS(f.read(), lang='en', tld='us')
        tts.save(f"translated-audio-{input_video_name}.wav")
    except Exception as e:
        print(f"[Line 193] Error text to speech: {e}.")
        return None


def add_translated_audio_to_video():
    try:
        # remove original audio
        input_video = ffmpeg.input(f"output-{input_video_name}.mp4", an=None)

        # add translated audio
        input_audio = ffmpeg.input(
            f"translated-audio-{input_video_name}.wav").audio
        stream = ffmpeg.concat(input_video, input_audio,
                               v=1, a=1)
        stream = ffmpeg.output(stream, f"final-{input_video_name}.mp4")
        ffmpeg.run(stream, overwrite_output=True)
    except Exception as e:
        print(f"[Line 203] Error add translared audio to video: {e}.")
        return None


def run():
    extract_audio()
    # split_audio()
    clean_audio()
    source_audio = f"clean-audio-{input_video_name}.wav"
    language, segments = transcribe_audio(source_audio)

    subtitle_file = generate_subtitle_file(
        translated=True, language=language, segments=segments
    )
    text_to_speech(f"translated-{input_video_name}.txt", 'en')

    add_subtitle_to_video(
        soft_subtitle=True,
        subtitle_file=f"sub-{input_video_name}-{out_lan}.srt",
        subtitle_language=language
    )

    add_translated_audio_to_video()

    if os.path.isfile(f"clean-audio-{input_video_name}.wav"):
        os.remove(f"clean-audio-{input_video_name}.wav")
    if os.path.isfile(f"audio-{input_video_name}.wav"):
        os.remove(f"audio-{input_video_name}.wav")
    if os.path.isfile(f"transcribed-{input_video_name}.txt"):
        os.remove(f"transcribed-{input_video_name}.txt")
    if os.path.isfile(f"output-{input_video_name}.mp4"):
        os.remove(f"output-{input_video_name}.mp4")
    if os.path.isfile(f"translated-audio-{input_video_name}.wav"):
        os.remove(f"translated-audio-{input_video_name}.wav")

run()
