from model.model_utils import load_yolov8_model, run_inference_and_save
import openai
import os

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

def generate_description(image_data):
    openai.api_key = os.getenv('OPENAI_API_KEY')

    # Construct a prompt based on your requirements
    prompt = f"Describe the following image: {image_data}"

    response = openai.Completion.create(
      engine="davinci",
      prompt=prompt,
      max_tokens=100
    )

    return response.choices[0].text.strip()
