import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import requests
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

UPLOAD_DIR = os.environ.get('UPLOAD_DIR', 'uploads')
ALLOWED_EXTENSIONS = {'wav','mp3','m4a','ogg'}
TRANSCRIBE_API_URL = os.environ.get('TRANSCRIBE_API_URL','http://127.0.0.1:9000')
TRANSCRIBE_ENDPOINT = os.environ.get('TRANSCRIBE_ENDPOINT','/transcribe')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR
app.secret_key = os.environ.get('FLASK_SECRET','dev-secret')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
load_dotenv()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    lang = request.form.get('language','en')
    temperature = request.form.get('temperature','0.0')
    if file.filename == '':
        return redirect(url_for('index'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        # forward file to transcribe API
        files = {'file': open(path, 'rb')}
        data = {'language': lang, 'temperature': temperature}
        try:
            resp = requests.post(TRANSCRIBE_API_URL + TRANSCRIBE_ENDPOINT, files=files, data=data, timeout=30)
            resp.raise_for_status()
            text = resp.text
        except Exception as e:
            app.logger.error(f"Error calling transcribe API: {e}")
            text = "An error occurred while processing your request. Please try again later."
        finally:
            files['file'].close()
        keep = os.environ.get('KEEP_UPLOADS','0')
        if keep != '1':
            try:
                os.remove(path)
            except Exception:
                pass
        return render_template('result.html', transcript=text)
    return redirect(url_for('index'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_DEBUG','0')=='1')
