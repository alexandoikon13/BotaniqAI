import torch
from PIL import Image
from io import BytesIO

# Function to load the YOLOv8 model
def load_yolov8_model():
    model = torch.hub.load('ultralytics/yolov8', 'yolov8', pretrained=True)
    return model

# Function to run inference
def run_inference(model, file_stream):
    # Convert file stream to PIL Image
    image = Image.open(BytesIO(file_stream.read()))

    # Perform inference
    results = model(image)

    # Process the results (e.g., draw bounding boxes)
    # This part depends on how you want to display the results.
    # For simplicity, let's just save the results as an image.
    results_image_path = 'path/to/save/results.jpg'
    results.save(results_image_path)

    return results_image_path
