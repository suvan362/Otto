from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import pymupdf

app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
app.config['UPLOAD_FOLDER']="./uploads"
app.secret_key = 'secretkey'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET'])
def upload_file():
    return render_template('upload.html')

@app.route('/Processed', methods=['POST'])
def file_details():
    text=""
    if 'file' not in request.files:
        flash('No file part, invalid request')
        return redirect(url_for('upload_file'))
    file = request.files['file']
    if not file:
        flash('No file uploaded, please upload a pdf file')
        return redirect(url_for('upload_file'))
    if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
        file.save(file_path)
        doc=pymupdf.open(file_path)
        for page in doc:
            text+=page.get_text()
        
        file_data = {
            "filename": filename,
            "content": text,
            "uploaded_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        doc.close()
        os.remove(file_path)
        return render_template('file_details.html',file=file_data)
    else:
        flash('File uploaded invalid, upload a valid .pdf file')
        return redirect(url_for('upload_file'))


if __name__ == '__main__':
    if not os.path.exists("./uploads"):
        os.makedirs("./uploads")
    app.run(debug=True)
