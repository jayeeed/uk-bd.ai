# Stage 3: Build Python Flask Server
# FROM ubuntu:latest
FROM python:3.10-slim

# Copy the rest of the Flask
# Update and install necessary packages
RUN apt-get update && \
    apt-get install -y python3.10 python3-pip && \
    apt-get install -y tesseract-ocr-ben && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /usr/src/app

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt && \
    pip uninstall bson -y && pip uninstall pymongo -y && \
    pip install pymongo

# Make port 5050 available to the world outside this container
EXPOSE 7050

# Define environment variable
ENV NAME Airbnb

# Copy the rest of your application files into the container
COPY . .

# Run app.py when the container launches
CMD ["python3", "app.py"]

