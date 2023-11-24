import torch

# Function to load the YOLOv8 model
def load_model():
    model = torch.hub.load('ultralytics/yolov8', 'yolov8', pretrained=True)  # Replace with the correct model
    return model

# Function to run inference
def run_inference(model, image_path):
    results = model(image_path)
    return results
