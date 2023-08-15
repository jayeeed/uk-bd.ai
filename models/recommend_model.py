from sklearn.preprocessing import OneHotEncoder
from sklearn.neighbors import NearestNeighbors
import pandas as pd
from bson import ObjectId
from db.db_config import get_data, recommended_collection

encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')

def preprocess_data(data_df):
    categorical_features = ["property_type", "amenities", "seasonality", "bed_type", "cancellation_policy"]
    numerical_features = ["number_of_bedrooms", "base_price", "estimated_monthly_bookings", "bathrooms",
                          "cleaning_fee", "host_response_rate", "number_of_reviews", "review_scores_rating", "beds"]

    encoded_features = encoder.fit_transform(data_df[categorical_features])
    all_features = pd.concat([data_df[numerical_features], pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(categorical_features))], axis=1)

    return all_features

def train_model(all_features):
    model = NearestNeighbors(n_neighbors=6, metric='euclidean')
    model.fit(all_features)
    
    return model

def get_recommendations(data):
    data_df = get_data()

    all_features = preprocess_data(data_df)
    model = train_model(all_features)

    user_params = [data["number_of_bedrooms"], data["base_price"], data["estimated_monthly_bookings"], data["bathrooms"],
                   data["cleaning_fee"], data["host_response_rate"], data["number_of_reviews"], data["review_scores_rating"], data["beds"],
                   *[1 if data["property_type"] == category else 0 for category in encoder.categories_[0]],
                   *[1 if amenity in data["amenities"] else 0 for amenity in encoder.categories_[1]],
                   *[1 if data["seasonality"] == category else 0 for category in encoder.categories_[2]],
                   *[1 if data["bed_type"] == category else 0 for category in encoder.categories_[3]],
                   *[1 if data["cancellation_policy"] == category else 0 for category in encoder.categories_[4]]
                   ]

    user_params = [user_params]
    _, indices = model.kneighbors(user_params)

    recommended_property_ids = data_df.iloc[indices[0][1:], data_df.columns.get_loc('property_id')].tolist()
    
    return recommended_property_ids
    
def save_recommendations(_id, search_params, recommended_property_ids):
    save_id = ObjectId(_id)  # Convert user_id to ObjectId
    
    # Update the document for the user with a new "search_parameters" array
    recommended_collection.update_one(
        {"_id": save_id},
        {"$push": {"search_parameters": search_params},
         "$set": {"recommended_properties": recommended_property_ids}},
        upsert=True  # Create a new document if user_id_obj doesn't exist
    )
    
def save_success(_id, selected_property_id):
    success_id = ObjectId(_id)  # Convert user_id to ObjectId
    
    recommended_collection.update_one(
        {"_id": success_id, "recommended_properties": selected_property_id},
        {"$set": {"success": selected_property_id}}
    )

