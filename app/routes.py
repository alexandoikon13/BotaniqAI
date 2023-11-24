from flask import Blueprint, render_template, request
from .utils import process_image  # Assuming you'll define this function

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    
    # Process the uploaded file
    output, description = process_image(file)   # 'process_image' is a placeholder function where you'll add the logic for image processing and OpenAI API interaction
    return render_template('results.html', image=output, description=description)
