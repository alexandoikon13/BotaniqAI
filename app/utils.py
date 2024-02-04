from model.model_utils import load_yolov8_model, run_inference_and_save
import requests

# Load the model (consider doing this when starting the app)
model = load_yolov8_model()

def process_image(file, cloudcube_url):
    # Run YOLOv8 inference
    file.stream.seek(0)  # Important: seek to the beginning of the file
    # Run YOLOv8 inference and save results in Cloudcube
    cloudcube_results_url = run_inference_and_save(model, file.stream, cloudcube_url)

    # Generate a description using OpenAI API
    description = generate_description(cloudcube_results_url)

    return cloudcube_results_url, description

def generate_description(image_url):
    try:
        response = requests.post('http://localhost:5000/generate', json={'text': f"Describe this image: {image_url}"})
        if response.status_code == 200:
            data = response.json()
            return data['generated_text']
        else:
            return "Error in generating description"
    except Exception as e:
        return f"An error occurred: {e}"
