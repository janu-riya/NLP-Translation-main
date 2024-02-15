from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi


def youtube_translate(url):
    video_id = url.split("=")[1]
    YouTubeTranscriptApi.get_transcript(video_id)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    result = ""
    for i in transcript:
        result += ' ' + i['text']
    
    return result



