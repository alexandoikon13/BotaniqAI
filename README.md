# BotaniqAI: AI-Powered Plant Detection &amp; Description
BotaniqAI is a sophisticated web application designed to analyze and identify plants in images using advanced object detection algorithms. Leveraging the power of YOLOv8 and OpenAI's GPT, this app provides insightful descriptions of detected plant species, making it an invaluable tool for botanists, hobbyists, and nature enthusiasts.

## Features
- Image Processing: Utilizes YOLOv8 for cutting-edge object detection.
- AI-Powered Descriptions: Generates descriptive text about detected plants using OpenAI's API.
- Cassandra Database Integration: Efficiently stores image metadata and processing results.
- User-Friendly Interface: Easy upload and review of images and results.
- Cloud Storage: Uses Cloudcube for organized and secure storage of images.
- Containerized Deployment: Docker (and locally with Kubernetes) ensure scalable and reliable deployment on Heroku.

## Technologies Used
- Frontend: HTML, CSS, JavaScript
- Backend: Python, Flask
- AI and ML: PyTorch, YOLOv8, OpenAI API
- Database: Cassandra
- Cloud Storage: Cloudcube
- Containerization and Orchestration: Docker, Kubernetes (local development/deployment with Minikube)
- Deployment Platform: Heroku

## Usage
- Navigate to the home page.
- Upload an image of a plant.
- View the processed image along with a detailed description of the detected plant species.

## License
Distributed under the MIT License. See 'LICENSE' for more information.
