from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import os
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Set upload folder
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        logger.warning("No file part in request.")
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        logger.warning("No file selected.")
        return redirect(request.url)
    
    try:
        # Save uploaded file
        filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        logger.info(f"File saved: {filename}")

        # Verify and resize image
        image = Image.open(filepath).convert("RGB")
        image = image.resize((800, 600))  # Resize for consistent display
        image.save(filepath)  # Overwrite with resized image
        logger.info(f"Image resized and saved: {filename}")

        return render_template('results.html', 
                             image=url_for('static', filename=f'uploads/{filename}'))
    
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return render_template('index.html', error=f"Error processing file: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)