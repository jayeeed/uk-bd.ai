from pymongo import MongoClient
import pandas as pd
import os, json
from dotenv import load_dotenv

load_dotenv()
COSMOSDB_CONN = os.getenv('COSMOSDB_CONN')
mongoAtlas = os.getenv('MONGDB_URI')
DATABASE_URL = os.getenv('DATABASE_URL')
print(type(mongoAtlas))

client = MongoClient(DATABASE_URL)


db = client['airbnb']

collections = ["allproperties","amenities","bookings","description","payments","prediction","recommended_properties","reviews","typeofplaces","users","wishlists"]


# Initialize your collection
for collection in collections:
    print(collection)
    init_collection = db[collection]

    json_file_name = "airbnb."+collection+".json"
    json_file_path = 'dataJson/'+json_file_name

    # Check if the JSON file exists
    if not os.path.exists(json_file_path):
        init_collection.insert_one({"collectionName":collection,"created":True})
    else:
        # Load your JSON data
        with open(json_file_path) as f:
            data = json.load(f)

        # Modify _id fields
        for doc in data:
            if '_id' in doc and '$oid' in doc['_id']:
                doc['_id'] = doc['_id']['$oid']

        # Insert data into the collection
        init_collection.insert_many(data)

        print(f"Data inserted successfully into {collection}.")



user_collection =db["users"]
properties_collection = db['allproperties']
recommended_collection = db['recommended_properties']
bookings_collection = db['bookings']
price_prediction = db["prediction"]
description_collection = db["description"] 
review_collection = db['reviews']


def get_data():
    data_from_mongodb = properties_collection.find()
    data_df = pd.DataFrame(data_from_mongodb)
    return data_df













# client = MongoClient('mongodb://e-state-db:fIyl4EwvEG34NxzhnwyAqJLreVDbqFpNnyPAIwsAWfwAKYurQ3SqqFe9xRQ2Sisg29vx9i2j6QhvACDbZzq40w==@e-state-db.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@e-state-db@')