import pymongo
from pymongo import MongoClient
import json

# Your Cosmos DB connection string
# cosmos_connection_string ='mongodb://e-state-db:fIyl4EwvEG34NxzhnwyAqJLreVDbqFpNnyPAIwsAWfwAKYurQ3SqqFe9xRQ2Sisg29vx9i2j6QhvACDbZzq40w==@e-state-db.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@e-state-db@'

mongoAtlas = "mongodb+srv://ipsita:Ipsita%402023@uk-bd0.u3pngqk.mongodb.net/"

local_database = "mongodb://localhost:27017"

# Connect to Cosmos DB
# client = MongoClient(mongoAtlas)
client = MongoClient(local_database)

# Specify the database and collection
database_name = "airbnb"
collection_name = "reviews"
db = client[database_name]
collection = db[collection_name]

# Path to your JSON file
json_file_path = "path/to/your/json_file.json"

# Read data from the JSON file
with open(json_file_path, 'r') as file:
    data_to_insert = json.load(file)

# Insert data into the collection
result = collection.insert_many(data_to_insert)

# Print the inserted document IDs
print("Inserted IDs:", result.inserted_ids)
