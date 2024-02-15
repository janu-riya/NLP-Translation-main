# Import the required module for text
# to speech conversion
from gtts import gTTS

# This module is imported so that we can
# play the converted audio
import os

# Language in which you want to convert
# tamil - ta , english - en ,hindi- hi, telugu - te, malayalam - ma
language_code = {'Bengali': 'bn', 'Gujarati': 'gu', 'Hindi': 'hi', 'Kannada': 'kn', 'Malayalam': 'ml', 'Tamil': 'ta', 'en-in': 'English (India)'}


def text_to_audio(translation_text, language, path):
    lan = language_code[language]
    myobj = gTTS(text=translation_text, lang=lan, slow=False)
    myobj.save(path)
    return path