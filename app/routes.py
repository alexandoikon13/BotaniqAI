from flask import Blueprint, render_template, request, jsonify
from werkzeug.utils import secure_filename
from .utils import process_image
from urllib.parse import urlparse
import secrets  # Python standard library for generating secure tokens
import logging
import uuid
import os
import threading
import time

# Global dictionary to store task status
task_status = {}

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
            task_id = str(uuid.uuid4())
            task_token = secrets.token_urlsafe()  # Generate a secure token
            thread = threading.Thread(target=process_file_async, args=(file, task_id))
            thread.start()
            task_status[task_id] = {"status": "Processing", "token": task_token}
            return jsonify({"task_id": task_id, "token": task_token}), 202
        else:
            return 'File type not allowed', 400
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return "An error occurred during upload.", 500

def process_file_async(file, task_id):
    start_time = time.time()
    try:
        # Fetch Cloudcube URL from environment variables
        cloudcube_url = urlparse(os.getenv('CLOUDCUBE_URL'))
        output, description = process_image(file, cloudcube_url)
        task_status[task_id] = {"status": "Complete", "image": output, "description": description}
    except Exception as e:
        logging.error(f"Error processing file: {e}")
        task_status[task_id] = {"status": "Error", "message": str(e)}
    finally:
        # Mark the task for deletion after a certain time
        task_status[task_id]['delete_at'] = time.time() + 600  # 10 minutes later

# Periodic cleanup function (could be run in a separate thread or scheduled task)
def cleanup_tasks():
    current_time = time.time()
    for task_id, info in list(task_status.items()):
        if info.get('delete_at', 0) < current_time:
            del task_status[task_id]


@main.route('/status/<task_id>', methods=['GET'])
def check_status(task_id):
    token = request.args.get('token')
    status = task_status.get(task_id, {"status": "Not Found"})

    # Check if the token matches
    if status.get("token") != token:
        return jsonify({"status": "Unauthorized"}), 401

    return jsonify(status)