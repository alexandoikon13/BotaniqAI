import boto3
from PIL import Image, ImageDraw
from io import BytesIO
from ultralytics import YOLO
import uuid
import os


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

    # Show the results
    for r in results:
        im_array = r.plot()  # plot a BGR numpy array of predictions
        im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image

    # Save the image with detections locally
    local_results_path = f"results/{str(uuid.uuid4())}.jpg"
    im.save(local_results_path)

    # Upload the results to Cloudcube
    s3 = boto3.client('s3')
    bucket_name = cloudcube_url.split('.')[0].split('//')[1]
    object_name = f"processed/{os.path.basename(local_results_path)}"
    s3.upload_file(local_results_path, bucket_name, object_name)

    # Return the URL of the saved image in Cloudcube
    cloudcube_results_url = f"{cloudcube_url}{object_name}"
    return cloudcube_results_url
