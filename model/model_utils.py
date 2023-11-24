import torch

def load_yolov8_model():
    # Load the YOLOv8 model
    model = torch.hub.load('ultralytics/yolov8', 'yolov8', pretrained=True)
    return model
