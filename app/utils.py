from model.model_utils import load_yolov8_model, run_inference
import openai


# Load the model (consider doing this when starting the app)
model = load_yolov8_model()

def process_image(file):
    # Run YOLOv8 inference
    file.stream.seek(0)  # Important: seek to the beginning of the file
    processed_image_path = run_inference(model, file.stream)

    # Generate a description using OpenAI API
    description = generate_description(processed_image_path)

    return processed_image_path, description

def generate_description(image_data):
    openai.api_key = 'your-api-key'

    # Construct a prompt based on your requirements
    prompt = f"Describe the following image: {image_data}"

    response = openai.Completion.create(
      engine="davinci",
      prompt=prompt,
      max_tokens=100
    )

    return response.choices[0].text.strip()
