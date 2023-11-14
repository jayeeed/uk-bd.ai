import requests
from pathlib import Path
# get the current working directory
current_working_directory = Path.cwd()
print(current_working_directory)

# set up the URL of your Flask API route
url = 'http://127.0.0.1:5050/upload'

# set up the request headers (optional)
headers = {'Content-Type': 'multipart/form-data'}

# set up the request payload with the file to upload
import os

filename = 'uploaded_data_file.jpg'
filepath = os.path.join(current_working_directory, filename)
print(filepath)

try:
    with open(filepath, 'rb') as f:
        files = {'file': (filename, f)}
        response = requests.post(url, headers=headers, files=files)
    print(files)
except FileNotFoundError:
    print(f"File not found at {filepath}")

# send the request to the Flask API route
# response = requests.post(url, headers=headers, files=files)

# print the response content
print(response.json())
print(response.content)
# print(response)