from flask import Flask
#from pathlib import Path
# from flask_cors import CORS

import pytesseract
#from pdf2image import convert_from_path
from PIL import Image

import re
import io
import time
import os


# CONFIGARATIONS

# get the current working directory
current_working_directory = os.getcwd()
print(current_working_directory)

extract_texts_file = current_working_directory + "instant_varification/output/output_of_scanned_image_to_text.txt"

searched_data_file = current_working_directory + "instant_varification/output/searched_data_file.txt"

searched_file = "output\searched_to_text.txt"


searched_lines=[]


# app = Flask(__name__, 
# template_folder='../templates',
# static_folder='../static')

# CORS(app)

# from ocr_app import routes