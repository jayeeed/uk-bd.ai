from features.instant_varification import os, current_working_directory
from . import ai_methods, regx_im, invoice_check
def file_upload_uitls(file):
    filename = 'uploaded_data_file' + "." + file.filename.rsplit(".", 1)[1]
    file.save(os.path.join(str(current_working_directory) + "/static/temp/" + filename))
    
    # assuming text_extracter() returns text as a string
    ai_methods.text_extracter(filename)  
    
    regex_data = regx_im.text_to_info()
    return regex_data

def id_verification(regex_data):
    invoice_matched =  invoice_check.info_matching(regex_data)
    print(invoice_matched)
    return {'success': invoice_matched}