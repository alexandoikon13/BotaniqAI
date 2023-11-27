import boto3
import torch
from PIL import Image
from io import BytesIO
from ultralytics import YOLO
import uuid


# Function to load the YOLOv8 model
def load_yolov8_model():
    # Load a pretrained YOLO model (recommended for training)
    model = YOLO('yolov8n.pt')
    return model

# Function to run inference and save results in Cloudcube
def run_inference_and_save(model, file_stream, cloudcube_url):
    # Convert file stream to PIL Image
    image = Image.open(BytesIO(file_stream.read()))

    # Perform inference
    results = model(image)

    # Save results as an image locally
    local_results_path = f"results/{str(uuid.uuid4())}.jpg"
    results.save(local_results_path)

    # Upload the results to Cloudcube
    s3 = boto3.client('s3')
    bucket_name = cloudcube_url.split('.')[0].split('//')[1]
    object_name = f"processed/{str(uuid.uuid4())}.jpg"
    s3.upload_file(local_results_path, bucket_name, object_name)

    # Return the URL of the saved image in Cloudcube
    cloudcube_results_url = f"{cloudcube_url}{object_name}"
    return cloudcube_results_url
