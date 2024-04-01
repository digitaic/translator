import time
import math
import ffmpeg
from googletrans import Translator
from faster_whisper import WhisperModel

translator = Translator()

source_location = 'source/video/'
#input_video = 'clase-15.mp4'
input_video = 'he.mp4'
# input_video = 'audio-spa.wav'
input_video_name = input_video.replace(".mp4", "")
# input_video_name = input_video.replace(".wav", "")
extracted_audio_location = 'process/audio/'
transcribed_text = 'transcribed.txt'
out_lan = 'en'


def extract_audio():
    extracted_audio = f"audio-{input_video_name}.wav"
    stream = ffmpeg.input(input_video)
    # stream = ffmpeg.output(stream, f"{extracted_audio_location}{extracted_audio}")
    stream = ffmpeg.output(stream, f"{extracted_audio}")
    ffmpeg.run(stream, overwrite_output=True)
    return extracted_audio


def transcribe(audio):
    model = WhisperModel('medium')
    segments, info = model.transcribe(audio, beam_size=3)
    language = info[0]
    print("Transcription Language ", info[0], info.language_probability)
    segments = list(segments)
    # f = open('transcribed.txt', 'w')
    for segment in segments:
        # print(segment)
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end,
              translate_text(segment.text, 'es', 'en')))
        # f.write(str(segment.text))
    return language, segments


def detect_input_language(text):
    input_lan = translator.detect(text)
    print(input_lan)
    return input_lan


def translate_text(text, input_lan, out_lan):
    t = translator.translate(text, src=input_lan, dest=out_lan)
    return str(t.text)
    # f = open('res.txt', 'w')
    # f.write(str(t.text))


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
    subtitle_file = f"sub-{input_video_name}.{language}.srt"
    text = ""
    if translated:
        for index, segment in enumerate(segments):
            segment_start = format_time(segment.start)
            segment_end = format_time(segment.end)
            text += f"{str(index+1)} \n"
            text += f"{segment_start} --> {segment_end} \n"
            text += f"{translate_text(segment.text, language, out_lan)} \n"
            text += "\n"
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


def run():
    extracted_audio = extract_audio()
    language, segments = transcribe(extracted_audio)
    subtitle_file = generate_subtitle_file(
        translated=True, language=language, segments=segments)

    add_subtitle_to_video(
        soft_subtitle=True,
        subtitle_file=subtitle_file,
        subtitle_language=language
    )


run()
