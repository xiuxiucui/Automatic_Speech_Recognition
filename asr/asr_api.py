from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import librosa
import sys


app = Flask(__name__)
tokenizer = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")
# Setup upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def load_and_resample_audio(audio_path, target_sr=16000):
    audio_data, sr = librosa.load(audio_path, sr=None)
    if sr != target_sr:
        audio_data = librosa.resample(audio_data, orig_sr=sr, target_sr=target_sr)
    # Calculate duration in seconds
    duration = librosa.get_duration(y=audio_data, sr=target_sr)
    return audio_data, duration


def transcribe_audio(tokenizer, model, audio_path):
    audio_input, duration = load_and_resample_audio(audio_path)
    input_values = tokenizer(audio_input, return_tensors="pt", sampling_rate=16000).input_values
    with torch.no_grad():
        logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = tokenizer.decode(predicted_ids[0])
    return transcription, duration


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({"response": "pong"})


@app.route('/asr', methods=['POST'])
def asr_endpoint():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        try:
            transcription, duration = transcribe_audio(tokenizer, model, file_path)
            print(transcription, file=sys.stdout)
        finally:
            # Cleanup: remove the file after processing
            os.remove(file_path)

        return jsonify({"transcription": transcription, "duration": duration}), 200

    return jsonify({"error": "File processing error"}), 500


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8001)
