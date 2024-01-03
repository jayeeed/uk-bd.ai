# Stage 2: Build Python Flask Server
FROM python:3.11.6 as flask-server-builder

# Set the working directory
WORKDIR /usr/src/app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install Flask dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Flask server code
COPY . .

# Expose the port on which the Flask server will run
EXPOSE 5000

# Start the Flask server
CMD ["python", "app.py"]
