import re
import fitz
from PIL import Image, ImageFilter
from features.instant_varification import os, current_working_directory, extract_texts_file, searched_data_file, io, pytesseract
#from ocr_app.utils.regx_im import text_open

# Check if we are on Windows and set the path to the Tesseract executable accordingly
if os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

else:
	pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"




def file_output(extracted_text):
    try:
        if not os.path.exists("output"):
            os.makedirs("output")
        # file_write_the_ocr_out = open("output/output_of_scanned_image_to_text.txt", "w")
        file_write_the_ocr_out = open(extract_texts_file, "w")
        
        for line in extracted_text:
            file_write_the_ocr_out.write(line)
        file_write_the_ocr_out.close()
        print('array data ==> "output_of_scanned_image_to_text".txt ')
    except Exception as e:
        print(e)


def pdf_process(file):
    pdf_file = os.path.join(str(current_working_directory)+'/static/temp/', file)
    # Open the PDF file using PyMuPDF and convert it into a list of JPEG images
    pdf = fitz.open(pdf_file)
    print("\nConverting the PDF into JPEG images...")
    image_list = []
    for i, page in enumerate(pdf):
        # Get the pixmap data as bytes
        pixmap = page.get_pixmap()
        pixmap_data = pixmap.samples
        # Convert the pixmap data into a PIL Image object
        img = Image.frombytes(
            mode="RGB", size=(pixmap.width, pixmap.height), data=pixmap_data
        )
        # Convert the PIL Image object to a JPEG and append it to the list
        with io.BytesIO() as tmp:
            img.convert("RGB").save(tmp, "jpeg", quality=90)
            image_list.append(tmp.getvalue())
    print("Conversion done!")

    # Extract text from the JPEG images using pytesseract
    extracted_text = []
    print("\nExtracting text using pytesseract...")
    for i, image in enumerate(image_list):
        with Image.open(io.BytesIO(image)) as img:
            text = pytesseract.image_to_string(img, lang="eng+ben")
            extracted_text.append(text)
        print(f"Page {i+1}: {len(text)} characters")
    print("Pdf Extraction done!")

    # Print the extracted text for each page
    # for i, text in enumerate(extracted_text):
    #     print(f"--- Page {i+1} ---")
    #     print(text, "\n")
    # print("\n extraction done...")

    file_output(extracted_text)


def image_pre_process(image_path):
    # Load input image
    image = Image.open(image_path)

    # Convert image to grayscale
    gray = image.convert("L")

    # # Binarize the image using Otsu's method
    # binary = gray.point(lambda x: 255 if x > 128 else 0, '1')

    # # Apply median filter to remove noise
    # thresholded = binary.filter(ImageFilter.MedianFilter(size=3))

    # Apply Gaussian blur to remove noise
    blurred = gray.filter(ImageFilter.GaussianBlur(radius=0.9))
    # Binarize the image using thresholding
    thresholded = blurred.point(lambda x: 255 if x > 128 else 0, mode="1")
    print(" \n image blured and thresholded successful ")
    return thresholded


def image_to_text(func):
    def wrapper(img_file):
        image_path = os.path.join(str(current_working_directory)+'/static/temp/', img_file)
        pre_processed_image = image_pre_process(image_path)
        extracted_text = pytesseract.image_to_string(pre_processed_image, lang="eng+ben")
        file_output(extracted_text)
        return func()
    return wrapper


@image_to_text
def image_processing():
    print("\n extraction done... \n")









# def image_processing(img_file):
#     image_path =  os.path.join(str(current_working_directory)+'/static/temp/', img_file)
#     # print(image_path)

#     pre_processed_image = image_pre_process(image_path)

#     extracted_text = pytesseract.image_to_string(pre_processed_image, lang="eng+ben")

#     file_output(extracted_text)

#     print("\n extraction done...")




# import pytesseract
# # Load input image and perform preprocessing
# image_path = 'nid.jpg'
# #image_path = 'id_card.jpg'
# preprocessed_image = image_preprocess(image_path)
# # Apply OCR on the preprocessed image
# text = pytesseract.image_to_string(preprocessed_image, lang='eng+ben')
# print(text)
