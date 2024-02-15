### install moviepy library ###

# pip install moviepy

# this function will combine audio and video files to file.

from moviepy.editor import *

import os

def combine_audio_video(vpath, apath, cvpath):

    videoclip = VideoFileClip(vpath)

    audioclip = AudioFileClip(apath)

    video = videoclip.set_audio(audioclip)

    video.write_videofile(cvpath)

