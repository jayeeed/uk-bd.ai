#------------------------------------verify_routes----------------------------------------
from flask import Blueprint, request, jsonify
from flask_cors import CORS,cross_origin

# from features.instant_varification import os, current_working_directory
from features.instant_varification.utils import file_upload_uitls, id_verification, nid_update


verify_routes = Blueprint('verify_routes', __name__)


CORS(verify_routes, resources={r"/api/idVerification/*": {"origins": "http://localhost:3009/e-check"}})


@verify_routes.route('/api/idVerification/upload', methods=['POST'])
@cross_origin(supports_credentials=True)
def upload_file():
    """
    This function handles the file upload request for ID verification.
    It receives the file from the request, saves it to a temporary location,
    extracts text from it using an AI method, applies regular expressions to extract relevant information,
    and checks if the extracted data matches the format of an invoice. If the invoice is valid,
    a success message is returned, otherwise an error message is returned.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'File not found in request'},400)
    
    file = request.files['file']
    regex_data = file_upload_uitls(file)
    # print(regex_data)
    
    response_data = id_verification(regex_data)

    if response_data:   
        return jsonify(response_data)   
    
    return jsonify({'message':'Upload unsuccessfull!'}) 
    # return JsonResponse(status=status.HTTP_400_BAD_REQUEST)



@verify_routes.route('/api/idVerification/update', methods=['POST'])
@cross_origin(supports_credentials=True)
def update_entity():
    """
    This function handles the file upload request for updating an entity's NID.
    It receives the file and user ID from the request, saves it to a temporary location,
    extracts text from it using an AI method, applies regular expressions to extract relevant information,
    and updates the collection with the extracted data. If the update is successful, a success message is returned,
    otherwise an error message is returned.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'File not found in request'},400)
    
    file = request.files['file']
    regex_data = file_upload_uitls(file)

    # Get userID from the request form
    user_id = request.form.get('userId')

    # Call the function to update the collection
    updated = nid_update.update_collection(user_id, regex_data)

    if updated:
        return jsonify({'success':'NID OCR is completed! and stored'})
    else:
        return jsonify({'error': 'Failed to update the collection'},500)







    # print(request.headers)
    # print(request.form)
    # print(request.files)




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