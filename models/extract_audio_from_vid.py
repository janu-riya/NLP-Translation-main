# Code for extract a audio to video 
# https://www.codespeedy.com/extract-audio-from-video-using-python/
# pip install ffmpeg moviepy

import moviepy.editor as movie
import os


def vid_aud(path, filename, folder):
    videoClip = movie.VideoFileClip(os.path.join(path))
    aud_filename = filename.split('.')[0] + '.wav'
    videoClip.audio.write_audiofile(os.path.join(folder, aud_filename))
    aud_filepath = os.path.join(folder, aud_filename)
    return aud_filepath

