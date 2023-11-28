from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename
from .utils import process_image
import logging
import os

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return 'No file part', 400
        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.stream.seek(0)  # Reset file pointer
            # Fetch Cloudcube URL from environment variables
            cloudcube_url = os.getenv('CLOUDCUBE_URL')
            output, description = process_image(file, cloudcube_url)  # # process the uploaded file and pass cloudcube_url here
            return render_template('results.html', image=output, description=description)
        else:
            return 'File type not allowed', 400
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return "An error occurred during upload.", 500
