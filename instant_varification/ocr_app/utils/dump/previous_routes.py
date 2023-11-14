
  
from ocr_app import app
from flask import request, redirect, render_template,url_for, send_file 

from ocr_app import os, current_working_directory
from ocr_app.ai_methods import text_extracter
from ocr_app.language_processing import get_summery





# @app.route('/')
# def index():
#     return 'Welcome to my Flask app!'


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST' and request.FILES:
        file = request.files['file']
        filename = 'uploaded_data_file' + "." + file.filename.rsplit(".", 1)[1]
        file.save("static/temp/" + filename)
        #print(os.path.join(current_working_directory, filename))
        #file.save(os.path.join(current_working_directory, filename))
        text_extracter(filename)
        return redirect(url_for('results', 
        message='File uploaded successfully and OCR is completed!',filename=filename))
    return render_template('index.html')


@app.route('/result')
def results():
    try:
        with open('output/output_of_scanned_image_to_text.txt', 'r') as file:
            text = file.read()
            message = request.args.get('message')
            filename = request.args.get('filename')
            filename = "/temp/"+filename
        return render_template('result.html', message=message, text=text, filename=filename)
    except Exception as e:
        print(e)
        return '<h3> Error: could not load the text file, Invalid File Upload </h3>'

@app.route('/download', methods=['GET'])
def download_file():
    try:
        current_working_directory = os.getcwd()
        file_path = os.path.join(current_working_directory, 'output', 'output_of_scanned_image_to_text.txt')
        return send_file(file_path, as_attachment=True)
    except:
        return '<h3>Error: could not load the file, File not found </h3>'


@app.route('/summerize')
def summerize():
    try:
        summery = get_summery()
        return render_template('result.html', summery=summery)
    except Exception as e:
        print(e)
        return '<h3> Error: could not summerize text file </h3> <p> {{e}}<p/>'