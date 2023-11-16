from pymongo import MongoClient
import pandas as pd

client = MongoClient('mongodb+srv://ipsita:Ipsita%402023@uk-bd0.u3pngqk.mongodb.net/')

db = client['airbnb']
properties_collection = db['allproperties']
recommended_collection = db['recommended_properties']
bookings_collection = db['bookings']

def get_data():
    data_from_mongodb = properties_collection.find()
    data_df = pd.DataFrame(data_from_mongodb)
    return data_df
