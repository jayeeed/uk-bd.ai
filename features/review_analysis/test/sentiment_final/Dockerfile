# Use a base image with Python installed
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the application code into the container
COPY . .

# Set environment variables
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port your app runs on
RUN python -m nltk.downloader vader_lexicon
EXPOSE 5000

# Command to run the application
CMD ["flask", "run"]