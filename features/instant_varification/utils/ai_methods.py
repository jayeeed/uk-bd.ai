import time
import re
import fitz
from PIL import Image


from features.instant_varification.utils.image_preprocessing import *
# from instant_varification.ocr_app import os, current_working_directory, io, pytesseract
# from image_preprocessing import *





def pdf_file_reader_with_ocr(func):
    def inner(*args, **kwargs):
        file = args[0]
        if file.endswith(".pdf"):
            print("trying to read the pdf file ", end=" ")
            print(*["-" for i in range(4)], sep=" ", end="") #; time.sleep(0.1)
            
            pdf_process(file)

        elif file.endswith((".jpg", ".jpeg", ".png")):
            print("trying to read the image file ", end=" ")
            print(*["-" for i in range(4)], sep=" ", end="") #; time.sleep(0.1)

            image_processing(file)

        else:
            print("Invalid file type")

        return func(*args, **kwargs)

    return inner



@pdf_file_reader_with_ocr
def text_extracter(pdf):
    print("status: 200 OK")











# def pdf_file_reader_with_ocr(func):
#     def inner(*args, **kwargs):
#         file = args[0]
#         if file.endswith(".pdf"):
#             print("trying to read the pdf file ", end=" ")
#             for i in range(0, 4):
#                 print("-", end=" ")
#                 # time.sleep(.2)

#             pdf_file = os.path.join(current_working_directory, file)

#             # Open the PDF file using PyMuPDF and convert it into a list of JPEG images
#             pdf = fitz.open(filename=pdf_file)
#             print("\nConverting the PDF into JPEG images...")
#             image_list = []
#             for i, page in enumerate(pdf):
#                 # Get a PNG image of the page
#                 pixmap = page.getPixmap()
#                 resolution = 100.0  # Change this to vary the resolution
#                 pixmap = page.getPixmap(
#                     matrix=fitz.Matrix(resolution / 72.0, resolution / 72.0)
#                 )
#                 img = Image.open(io.BytesIO(pixmap.getImageData(output="png")))
#                 # Convert the PNG image to JPEG and append it to the list
#                 with io.BytesIO() as tmp:
#                     img.convert("RGB").save(tmp, "jpeg", quality=90)
#                     image_list.append(tmp.getvalue())
#             print("Conversion done!")

#             # Extract text from the JPEG images using pytesseract
#             extracted_text = []
#             print("\nExtracting text using pytesseract...")
#             for i, image in enumerate(image_list):
#                 with Image.open(io.BytesIO(image)) as img:
#                     text = pytesseract.image_to_string(img, lang="eng")
#                     extracted_text.append(text)
#                 print(f"Page {i+1}: {len(text)} characters")
#             print("Extraction done!")

#             # Print the extracted text for each page
#             # for i, text in enumerate(extracted_text):
#             #     print(f"--- Page {i+1} ---")
#             #     print(text, "\n")

#             print("\n extraction done...")
#             try:
#                 if not os.path.exists("output"):
#                     os.makedirs("output")
#                 file_write_the_ocr_out = open(
#                     "output/output_of_scanned_image_to_text.txt", "w"
#                 )
#                 for line in extracted_text:
#                     file_write_the_ocr_out.write(line)
#                 file_write_the_ocr_out.close()
#                 print('array data ==> "output_of_scanned_image_to_text".txt ')
#             except Exception as e:
#                 print(e)

#         elif file.endswith((".jpg", ".jpeg", ".png")):
#             print("trying to read the image file ", end=" ")
#             for i in range(0, 4):
#                 print("-", end=" ")
#                 # time.sleep(.1)

#             image_path = os.path.join(current_working_directory, file)
#             # print(image_path)

#             image = Image.open(image_path)
#             print(" \n image read successful")

#             extract = pytesseract.image_to_string(image)
#             print("\n extraction done...")
#             try:
#                 if not os.path.exists("output"):
#                     os.makedirs("output")
#                 file_write_the_ocr_out = open(
#                     "output/output_of_scanned_image_to_text.txt", "w"
#                 )
#                 file_write_the_ocr_out.write(extract)
#                 file_write_the_ocr_out.close()
#                 print('array data ==> "output_of_scanned_image_to_text".txt ')
#             except Exception as e:
#                 print(e)

#         else:
#             print("Invalid file type")

#         return func(*args, **kwargs)

#     return inner















# def pdf_file_reader_with_ocr(func):
#     def inner(*args, **kwargs):
#         file = args[0]
#         if file.endswith('.pdf'):
#             print("trying to read the pdf file ", end=' ')
#             for i in range(0,4):
#                 print('-', end=' ')
#                 #time.sleep(.2)


#             pdfFile = WiImage(filename= str(current_working_directory)+'/'+ file, resolution = 300)
#             print("\n converting the pdf into a jpeg file", end=' ')
#             for i in range(0,4):
#                 print('-', end=' ')
#                 #time.sleep(.2)
#             image = pdfFile.convert('jpeg')
#             print(" \n image conversion successful")

#             imageBlobs = []
#             for img in image.sequence:
#                 imgPage = WiImage(image = img)
#                 imageBlobs.append(imgPage.make_blob('jpeg'))

#             extract = []
#             print(" \n extracting texts", end=' ')
#             for i in range(0,4):
#                 print('-', end=' ')
#                 #time.sleep(.1)
#             for imgBlob in imageBlobs:
#                 image = Image.open(io.BytesIO(imgBlob))
#                 text = pytesseract.image_to_string(image, lang = 'eng')
#                 extract.append(text)

#             print('\n extraction done...')
#             try:
#                 if not os.path.exists('output'):
#                     os.makedirs('output')
#                 file_write_the_ocr_out = open('output/output_of_scanned_image_to_text.txt', 'w')
#                 for line in extract:
#                     file_write_the_ocr_out.write(line)
#                 file_write_the_ocr_out.close()
#                 print('array data ==> "output_of_scanned_image_to_text".txt ')
#             except Exception as e:
#                 print(e)

#         elif file.endswith(('.jpg', '.jpeg', '.png')):
#             print("trying to read the image file ", end=' ')
#             for i in range(0,4):
#                 print('-', end=' ')
#                 #time.sleep(.1)

#             image_path = os.path.join(current_working_directory, file)
#             #print(image_path)

#             image = Image.open(image_path)
#             print(" \n image read successful")

#             extract = pytesseract.image_to_string(image)
#             print('\n extraction done...')
#             try:
#                 if not os.path.exists('output'):
#                     os.makedirs('output')
#                 file_write_the_ocr_out = open('output/output_of_scanned_image_to_text.txt', 'w')
#                 file_write_the_ocr_out.write(extract)
#                 file_write_the_ocr_out.close()
#                 print('array data ==> "output_of_scanned_image_to_text".txt ')
#             except Exception as e:
#                 print(e)

#         else:
#             print('Invalid file type')

#         return func(*args, **kwargs)
#     return inner



# if __name__=='__main__':
#     #pdf='\Hosain.pdf'
#     pdf='res.jpg'
#     text_extracter(pdf)
#     text_file_maker()
