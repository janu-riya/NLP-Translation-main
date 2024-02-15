import moviepy.editor as movie
from os import path
  
def vid_aud(filename):
    videoClip = movie.VideoFileClip(filename)
    videoClip.audio.write_audiofile("finalresult.wav")



