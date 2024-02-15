from sys import implementation
from flask import Flask, request, redirect, flash, send_from_directory, render_template, send_file
from werkzeug.utils import secure_filename
from models.audio_to_englishtxt import get_large_audio_transcription
from models.english_to_multilanguage import eng_to_mul
from models.transcript import youtube_translate
from models.txt_to_aud import text_to_audio
from models.extract_audio_from_vid import vid_aud
from models.merge_audio_to_video import combine_audio_video
from models.transliteration import transliteration_language,driver
from models.keyword_extraction import keyword
import os
from pydub import AudioSegment
from models.download import uvid_downlaod

'''# get current directory
path = os.getcwd()
# path of video file folder
vid_folderpath = os.path.join(path, 'Static_files\\Video')
#path of audio file folder
aud_folderpath = os.path.join(path, 'Static_files\\Audio') '''

app = Flask(__name__, static_url_path='/', static_folder='Static_files/')
app.config['SECRET_KEY'] = 'my secret'
app.config['UPLOADS_FOLDER'] = './Static_files/'
folder = app.config['UPLOADS_FOLDER']

@app.route("/", methods=["POST", "GET"])
def login():
    return render_template('login.html')

@app.route("/index", methods=["POST", "GET"])
def index():
    return render_template('index.html')

@app.route("/home", methods=["POST", "GET"])
def home():
    return render_template('index.html')

@app.route("/features", methods=["POST", "GET"])
def features():
    return render_template('features.html')


@app.route("/litfeatures", methods=["POST", "GET"])
def litfeatures():
    return render_template('lit_features.html')


@app.route("/textform", methods=["GET"])
def text_form():
    return render_template('textform.html')


@app.route("/text-to-text", methods=["POST"])
def text_to_text():
    text = request.form['text']
    lang = request.form['language']
    trans_txt = eng_to_mul(text, lang)
    translation_text = trans_txt[0]['translation_text']
    keyword_extract = keyword(text,lang)
    output = ""
    for i in keyword_extract:
        output += i + '  :  ' + transliteration_language(i,lang)+' ,  '
    filename = 'audio.mp3'
    path = os.path.join(app.config['UPLOADS_FOLDER'], filename)
    txt_audio = text_to_audio(translation_text, lang, path)
    return render_template('textoutput.html', translation_text= translation_text , vocabulary_text = output, path=path, filename=filename, text = text)
    

@app.route("/audioform", methods=["POST", "GET"])
def audio_form():
    return render_template('audio_to_audio.html')


@app.route("/audio-to-audio", methods=['GET', 'POST'])
def audio_to_audio():
    f = request.files["file"]
    lang = request.form['language']
    name = f.filename

    if not 'file' in request.files:
        flash('No file part in request')
        return redirect(request.url)

    if f.filename == '':
        flash('No file uploaded')
        return redirect(request.url)

    else:
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOADS_FOLDER'], filename))
        path = os.path.join(app.config['UPLOADS_FOLDER'], filename)
        text = get_large_audio_transcription(path)
        trans_text = eng_to_mul(text, lang) 
        translated_text = trans_text[0]['translation_text']
        audio_name = ('translated_'+filename).replace('.wav', '.mp3')
        audio_path = os.path.join(app.config['UPLOADS_FOLDER'], audio_name)
        txt_audio = text_to_audio(translated_text, lang, audio_path)
        return render_template('aud_output.html', translation_text=translated_text, path=audio_path, filename=audio_name)


@app.route("/videoform", methods=["POST", "GET"])
def video_form():
    return render_template('vid-vid.html')


@app.route("/video-to-video", methods=['GET', 'POST'])
def video_to_video():
    f = request.files["file"]
    lang = request.form['language']
    name = f.filename

    if not 'file' in request.files:
        flash('No file part in request')
        return redirect(request.url)

    if f.filename == '':
        flash('No file uploaded')
        return redirect(request.url)

    else:
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOADS_FOLDER'], filename))
        vid_path = os.path.join(app.config['UPLOADS_FOLDER'], filename)
        path = vid_aud(vid_path, filename, folder)
        text = get_large_audio_transcription(path)
        trans_text = eng_to_mul(text, lang)
        translated_text = trans_text[0]['translation_text']
        audio_name = ('translated_' + filename).replace('.mp4', '.mp3')
        audio_path = os.path.join(app.config['UPLOADS_FOLDER'], audio_name)
        txt_audio = text_to_audio(translated_text, lang, audio_path)
        combined_vid_path = os.path.join(app.config['UPLOADS_FOLDER'], 'combined_'+filename)
        combine_audio_video(vid_path, audio_path, combined_vid_path)
        combined_vid_filename = 'combined_' + filename
        return render_template('vid_out.html', translation_text=translated_text, path=combined_vid_path, filename= combined_vid_filename)



@app.route('/return-files/<path:path>', methods=['GET', 'POST'])
def return_file(path):
    return send_file(path)


@app.route("/youtubeform", methods=["POST", "GET"])
def youtube_form():
    return render_template('youtubeform.html')


@app.route("/youtube-youtube", methods=['GET', 'POST'])
def youtube_to_youtube():
    link = request.form['url']
    language = request.form['language']
    filename = 'youtube_video.mp4'
    you_path = os.path.join(folder, 'Youtube/')
    uvid_downlaod(link,you_path,filename )
    vid_path= os.path.join(you_path, filename)
    path = vid_aud(vid_path, filename, folder)
    text = get_large_audio_transcription(path)
    trans_text = eng_to_mul(text, language)
    translated_text = trans_text[0]['translation_text']
    audio_name = ('translated_' + filename).replace('.mp4', '.mp3')
    audio_path = os.path.join(app.config['UPLOADS_FOLDER'], audio_name)
    txt_audio = text_to_audio(translated_text, language, audio_path)
    combined_vid_path = os.path.join(app.config['UPLOADS_FOLDER'], 'combined_'+filename)
    combine_audio_video(vid_path, audio_path, combined_vid_path)
    combined_vid_filename = 'combined_' + filename
    return render_template('vid_out.html', translation_text=translated_text, path=combined_vid_path, filename= combined_vid_filename)


@app.route("/transliteration-form", methods=["GET"])
def transliteration_form():
    return render_template('txt-lit.html')


@app.route("/transtext-to-text", methods=["POST"])
def transtext_to_text():
    text = request.form['text']
    lang = request.form['language']
    if lang in ['Tamil', 'Kannada'] :
        trans_txt = transliteration_language(text, lang)
    else:
        trans_txt = driver(text, lang)
    filename = 'translitered_audio.mp3'
    path = os.path.join(app.config['UPLOADS_FOLDER'], filename)
    txt_audio = text_to_audio(trans_txt, lang, path)
    return render_template('textoutput.html', translation_text=trans_txt, path=path, filename=filename)

@app.route("/transliteration-audioform", methods=["GET"])
def transliteration_audio_form():
    return render_template('aud-lit.html')


@app.route("/transaudio-to-audio", methods=['GET', 'POST'])
def transaudio_to_audio():
    f = request.files["file"]
    lang = request.form['language']
    name = f.filename

    if not 'file' in request.files:
        flash('No file part in request')
        return redirect(request.url)

    if f.filename == '':
        flash('No file uploaded')
        return redirect(request.url)

    else:
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOADS_FOLDER'], filename))
        path = os.path.join(app.config['UPLOADS_FOLDER'], filename)
        text = get_large_audio_transcription(path)
        if lang in ['Tamil', 'Kannada'] :
            translated_text = transliteration_language(text, lang)
        else:
            translated_text = driver(text, lang)
        audio_name = ('translated_'+ filename).replace('.wav', '.mp3')
        audio_path = os.path.join(app.config['UPLOADS_FOLDER'], audio_name)
        txt_audio = text_to_audio(translated_text, lang, audio_path)
        return render_template('aud_output.html', translation_text=translated_text, path=audio_path, filename=audio_name)


@app.route("/transliteration-videoform", methods=["GET"])
def transliteration_video_form():
    return render_template('vid-lit.html')

@app.route("/transvideo-to-video", methods=['GET', 'POST'])
def transvideo_to_video():
    f = request.files["file"]
    lang = request.form['language']
    name = f.filename

    if not 'file' in request.files:
        flash('No file part in request')
        return redirect(request.url)

    if f.filename == '':
        flash('No file uploaded')
        return redirect(request.url)

    else:
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOADS_FOLDER'], filename))
        vid_path = os.path.join(app.config['UPLOADS_FOLDER'], filename)
        path = vid_aud(vid_path, filename, folder)
        text = get_large_audio_transcription(path)
        if lang in ['Tamil', 'Kannada'] :
            trans_txt = transliteration_language(text, lang)
        else:
            trans_txt = driver(text, lang)
        audio_name = ('translated_' + filename).replace('.mp4', '.mp3')
        audio_path = os.path.join(app.config['UPLOADS_FOLDER'], audio_name)
        txt_audio = text_to_audio(trans_txt, lang, audio_path)
        combined_vid_path = os.path.join(app.config['UPLOADS_FOLDER'], 'combined_'+filename)
        combine_audio_video(vid_path, audio_path, combined_vid_path)
        combined_vid_filename = 'combined_' + filename
        return render_template('vid_out.html', translation_text=trans_txt, path=combined_vid_path, filename= combined_vid_filename)


if __name__ == "__main__":
  app.run(debug=True)


