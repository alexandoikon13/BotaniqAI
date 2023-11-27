# Start from the PyTorch image with CUDA support
FROM pytorch/pytorch:1.8.1-cuda11.1-cudnn8-runtime

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py using gunicorn when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:5000", "--timeout 300", "run:app"]
