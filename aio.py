from flask import Flask, request, jsonify
from pymongo import MongoClient
from sklearn.preprocessing import OneHotEncoder
from sklearn.neighbors import NearestNeighbors
import pandas as pd

app = Flask(__name__)

# MongoDB configuration
client = MongoClient('mongodb+srv://xy3d:XgB8JVGTuWGd50kp@cluster0.20iimjx.mongodb.net/')
db = client['airbnb']
properties_collection = db['properties']
recommended_collection = db['recommended_properties']

# Load data from MongoDB into a DataFrame
data_from_mongodb = properties_collection.find()  # Modify query if needed
data_df = pd.DataFrame(data_from_mongodb)

# Categorical and numerical features
categorical_features = ["property_type", "amenities", "seasonality", "bed_type", "cancellation_policy"]
numerical_features = ["number_of_bedrooms", "base_price", "estimated_monthly_bookings", "bathrooms",
                      "cleaning_fee", "host_response_rate", "number_of_reviews", "review_scores_rating", "beds"]

# Perform one-hot encoding for categorical features
encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
encoded_features = encoder.fit_transform(data_df[categorical_features])

# Combine encoded features with numerical features
all_features = pd.concat([data_df[numerical_features], pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(categorical_features))], axis=1)

# Fit Nearest Neighbors model
model = NearestNeighbors(n_neighbors=6, metric='euclidean')  # Find 6 nearest neighbors (including itself)
model.fit(all_features)

@app.route('/api/search', methods=['POST'])
def search_properties():
    data = request.json  # Assuming you're sending JSON data in the request
    
    user_params = [
        data["number_of_bedrooms"], data["base_price"], data["estimated_monthly_bookings"], data["bathrooms"],
        data["cleaning_fee"], data["host_response_rate"], data["number_of_reviews"], data["review_scores_rating"], data["beds"],
        # Encode categorical features
        *[1 if data["property_type"] == category else 0 for category in encoder.categories_[0]],
        *[1 if amenity in data["amenities"] else 0 for amenity in encoder.categories_[1]],
        *[1 if data["seasonality"] == category else 0 for category in encoder.categories_[2]],
        *[1 if data["bed_type"] == category else 0 for category in encoder.categories_[3]],
        *[1 if data["cancellation_policy"] == category else 0 for category in encoder.categories_[4]]
    ]
    
    # Reshape user_params to match the shape of the preprocessed data
    user_params = [user_params]
    
    # Find the nearest neighbors (property indices) based on user parameters
    _, indices = model.kneighbors(user_params)
    
    # Extract the property IDs from the original DataFrame
    recommended_property_ids = data_df.iloc[indices[0][1:], data_df.columns.get_loc('property_id')].tolist()
    
    # Insert the search parameters and user_id into the "search" collection
    user_id = data.get("user_id")  # Assuming user_id is sent in the JSON request
    recommended_collection.insert_one({
        "user_id": user_id,
        "search_parameters": {key: value for key, value in data.items() if key != "user_id"},
        "recommended_properties": recommended_property_ids
    })
    
    return jsonify({"message": "Property search parameters saved and recommendations generated!"})

if __name__ == '__main__':
    app.run(debug=True)
