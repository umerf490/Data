from flask import Flask, render_template, request, jsonify, send_file
import speech_recognition as sr
from translate import Translator
from gtts import gTTS
import os
import uuid

app = Flask(__name__)

# Define directories for audio files
audio_dir = 'static/audio'
tts_dir = 'static/tts'

os.makedirs(audio_dir, exist_ok=True)
os.makedirs(tts_dir, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stt', methods=['POST'])
def speech_to_text():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file uploaded'})

    audio_file = request.files['audio']

    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        return jsonify({'text': text})
    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand audio'})

@app.route('/translate', methods=['POST'])
def translate_text():
    text = request.form.get('text', '')
    target = request.form.get('target', 'fr')

    if not text:
        return jsonify({'error': 'No text provided'})

    try:
        translator = Translator(to_lang=target)
        translation = translator.translate(text)
        return jsonify({'translation': translation})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/tts', methods=['POST'])
def text_to_speech():
    text = request.form.get('text', '')
    target_language = request.form.get('target_language', 'fr')

    if not text:
        return jsonify({'error': 'No text provided'})

    try:
        tts_filename = f'tts_{str(uuid.uuid4())}.mp3'

        tts = gTTS(text, lang=target_language)
        tts.save(os.path.join(tts_dir, tts_filename))

        return send_file(os.path.join(tts_dir, tts_filename), as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
