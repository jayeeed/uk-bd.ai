# --------------------------------------verify_routes----------------------------------------

from flask import Blueprint, request,jsonify,redirect, render_template,url_for, send_file 



from instant_varification.ocr_app import os, current_working_directory
from instant_varification.ocr_app.utils import ai_methods, regx_im, invoice_check, nid_update




verify_routes = Blueprint('verify_routes', __name__)



@verify_routes.route('/api/idVerification/upload', methods=['POST'])
def upload_file():
    print(request.headers)
    print(request.form)
    print(request.files)
    
    # if 'file' not in request.files:
    #     return {"error": "File not found in request"}, 400
    # else:
    #     print(request.files['file'])

    if 'file' not in request.files:
        return jsonify({'error': 'File not found in request'},400)
    
    file = request.files['file']
    filename = 'uploaded_data_file' + "." + file.filename.rsplit(".", 1)[1]
    file.save(os.path.join(str(current_working_directory) + "/static/temp/" + filename))
    
    ai_methods.text_extracter(filename)  # assuming text_extracter() returns text as a string
    
    regex_data = regx_im.text_to_info()

    # print(regex_data)

    invoice_matched =  invoice_check.info_matching(regex_data)

    print(invoice_matched)
    if invoice_matched:
        response_data = {'success': invoice_matched}
        return jsonify(response_data)
    
    return jsonify({'message':' Upload unsuccessfull! '})

 
    # return JsonResponse(status=status.HTTP_400_BAD_REQUEST)

    
    # return jsonify({'filename': filename, 'text': text})



@verify_routes.route('/api/idVerification/update', methods=['POST'])
def update_entity():
    print(request.headers)
    print(request.form)
    print(request.files)

    if 'file' not in request.files:
        return jsonify({'error': 'File not found in request'},400)
    
    file = request.files['file']

    # Get userID from the request form
    user_id = request.form.get('userId')

    filename = 'uploaded_data_file' + "." + file.filename.rsplit(".", 1)[1]
    file.save("static/temp/" + filename)
    
    ai_methods.text_extracter(filename)  # assuming text_extracter() returns text as a string
    
    regex_data = regx_im.text_to_info()

    # Call the function to update the collection
    updated = nid_update.update_collection(user_id, regex_data)

    if updated:
        return jsonify({'success':'NID OCR is completed! and stored'})
    else:
        return jsonify({'error': 'Failed to update the collection'},500)












#from flask import request, redirect, render_template,url_for, send_file ,jsonify
#from ocr_app.ai_methods import text_extracter
#from instant_varification.ocr_app.utils.language_processing import get_summery


# @verify_routes.route('/api/property/<property_id>', methods=['GET'])
# # def get_property_details(property_id):
# #     property_data = properties_collection.find_one({"property_id": int(property_id)})
    
# #     if property_data:
# #         # Convert ObjectId to a string for JSON serialization
# #         property_data['_id'] = str(property_data['_id'])
        
# #         return jsonify(property_data)
# #     else:
# #         return jsonify({"message": "Property not found"}), 404


# # /api/idVerification/upload







# @verify_routes.route('/result')
# def results():
#     try:
#         with open('output/output_of_scanned_image_to_text.txt', 'r') as file:
#             text = file.read()
#             message = request.args.get('message')
#             filename = request.args.get('filename')
#             filename = "/temp/"+filename
#         return render_template('result.html', message=message, text=text, filename=filename)
#     except Exception as e:
#         print(e)
#         return '<h3> Error: could not load the text file, Invalid File Upload </h3>'

# @verify_routes.route('/download', methods=['GET'])
# def download_file():
#     try:
#         current_working_directory = os.getcwd()
#         file_path = os.path.join(current_working_directory, 'output', 'output_of_scanned_image_to_text.txt')
#         return send_file(file_path, as_attachment=True)
#     except:
#         return '<h3>Error: could not load the file, File not found </h3>'


# @verify_routes.route('/summerize')
# def summerize():
#     try:
#         summery = get_summery()
#         return render_template('result.html', summery=summery)
#     except Exception as e:
#         print(e)
#         return '<h3> Error: could not summerize text file </h3> <p> {{e}}<p/>'
    
    
    
    
    
    
    
# const sendDataToEndpoint = async () => {
#   const response = await fetch('/your-endpoint-url', {
#     method: 'POST',
#     headers: {
#       'Content-Type': 'application/json',
#     },
#     body: JSON.stringify({ userId }),
#   });

#   // Handle the response
#   const data = await response.json();
#   console.log(data);
# };

# sendDataToEndpoint();