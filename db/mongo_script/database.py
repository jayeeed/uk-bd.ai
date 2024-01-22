import subprocess
subprocess.check_call(["python3", '-m', 'pip', 'install', 'pymongo'])
from pymongo import MongoClient
import json, os

# Create a client connection to your MongoDB instance
client = MongoClient('localhost', 27017)

# Initialize your database
db = client['airbnb']

if db !="None":
    print("connected")

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



