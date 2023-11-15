from instant_varification.ocr_app.utils.image_preprocessing import image_to_text
from instant_varification.ocr_app import extract_texts_file, searched_data_file, os ,re

#import os, re
# current_directory = os.getcwd()
#print("Current directory:", current_directory)

# extract_texts_file = current_directory+ "/output/output_of_scanned_image_to_text.txt"
# searched_data_file = current_directory+ "/output/searched_data_file.txt"



info = {}
key_list = ["ID NO", "Name:" ,"Date of Birth:"]

def text_open():
    searched_lines=[]

    with open(extract_texts_file, "r", encoding="utf-8") as f:
        for index, line in enumerate(f):
#Invoice no: 1699717261
            if re.search(r'ID NO:', line):
                    id_match = re.search(r'\d+', line)
                    if id_match:
                        info["nid"] = int(id_match.group())
            else:
                info["nid"] = ""
            
            if re.search(r'Invoice no:', line):
                    id_match = re.search(r'\d+', line)
                    if id_match:
                        info["invoiceNo"] = int(id_match.group())

            if re.search(r'Name:|Date of Birth:', line):
                if line not in searched_lines:
                    if "Name:" in line:
                        info["name"] = line.split(":")[1].strip() # extract and strip name
                    elif "Date of Birth:" in line:
                        info["dob"] = line.split(":")[1].strip() # extract and strip date of birth
            else:
                info["Name"] = ""
                info["Date of Birth:"] = ""
                

    with open(searched_data_file, "w") as fw:
        for key, value in info.items():
            fw.write(f"{key}: {value}\n")

    print(info)
    return info



#@image_to_text
def text_to_info():
    info = text_open()
    return info 


















# def file_stuff(func):
#     searched_lines = []
#     info = []

#     def file_browse():
#         with open(extract_texts_file, "r") as f:
#             for index, line in enumerate(f):
#                 if "Result/GPA" in line:
#                     print(line)
#                     if line not in searched_lines:
#                         searched_lines.append(line)
#                 if "Name: " in line:
#                     if line not in searched_lines:
#                         info.append(line)

#         # print(searched_lines)
#         # print(info)

#         with open(searched_file, "w") as fw:
#             for line in searched_lines:
#                 # print(type(line))
#                 fw.write(line)
#             for line in info:
#                 # print(type(line))
#                 fw.write(line)








# @file_stuff
# def text_file_maker(found_lines_for_regular_expression, info):
#     result_sum = 0
#     for line in found_lines_for_regular_expression:  # string = 'gpa:1.5 cgpa:5.0.'
#         pattern = "\d+"
#         result = re.findall(pattern, line)
#         num = total_gpa(result)
#         result_sum += num
#     info = json.dumps(info)
#     print(type(info))

#     print("Total Cgpa of 'HSC and Bachelor' Degree ==> {}".format(result_sum))












    

    # with open(extract_texts_file, "r",encoding="utf-8") as fr:
    #     for index, line in enumerate(fr):
    #         if re.search(r'ID NO:', line):
    #             #print(index+1, line)
    #             if line not in searched_lines:
    #                 searched_lines.append(line)
    #         if re.search(r'Name:', line):
    #             if line not in searched_lines:
    #                 info.append(line)

    # with open(searched_data_file, "w") as fw:
    #     for line in searched_lines:
    #         fw.write(line)
    #     for line in info:
    #         fw.write(line)