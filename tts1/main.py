from gtts import gTTS
from gtts.tokenizer import pre_processors
import gtts.tokenizer.symbols

TEXT = "Are you sure???  ... maybe there is a mistake?  Please check again.  I'll wait!... go on!"
 
""" 
pre_processor_funcs='preprocessor_funcs_list'
preprocessor_funcs_list = [
    pre_processors.tone_marks,
    pre_processors.end_of_line,
    pre_processors.abbreviations,
    pre_processors.word_sub
]
"""

tts = gTTS(
    TEXT,
    tld="us",
    lang="en",
    lang_check=True,
    )

tts.save('t.mp3')
