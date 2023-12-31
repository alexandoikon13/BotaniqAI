import boto3
from PIL import Image, ImageDraw
from io import BytesIO
from ultralytics import YOLO
from urllib.parse import urlparse
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
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    local_results_path = os.path.join(results_dir, f"{str(uuid.uuid4())}.jpg")
    im.save(local_results_path)

    # Prepare for upload to Cloudcube
    parsed_url = urlparse(os.environ.get('CLOUDCUBE_URL'))
    bucket_name = parsed_url.netloc.split('.')[0]

    with open(local_results_path, 'rb') as file_data:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('CLOUDCUBE_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('CLOUDCUBE_SECRET_ACCESS_KEY')
        )
        try:
            s3_client.put_object(
                Bucket=bucket_name,
                Key=f"{parsed_url.path[1:]}/results/{os.path.basename(local_results_path)}",
                Body=file_data,
                ContentType='image/jpeg'  # Adjust content type if necessary
            )
        except Exception as e:
            print(f"Failed to upload to S3: {e}")
            raise

    # Construct and return Cloudcube URL
    cloudcube_results_url = f"{cloudcube_url}{parsed_url.path[1:]}/results/{os.path.basename(local_results_path)}"
    return cloudcube_results_url
