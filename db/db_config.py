from pymongo import MongoClient
import pandas as pd

client = MongoClient('mongodb+srv://ipsita:Ipsita%402023@uk-bd0.u3pngqk.mongodb.net/')

db = client['airbnb']
user_collection =db["users"]
properties_collection = db['allproperties']
recommended_collection = db['recommended_properties']
bookings_collection = db['bookings']
price_prediction = db["prediction"]
description_collection = db["description"] 
chatbot_predicted_ques_ans_collection = db["chatbot_predicted_ques_ans"] 
chatbot_question_ans_collection = db["chatbot_question_ans"]
chatbot_human_ans_collection = db["chatbot_human_ans"]
# allProperties_collection =db['allproperties']

def get_data():
    data_from_mongodb = properties_collection.find()
    data_df = pd.DataFrame(data_from_mongodb)
    return data_df
