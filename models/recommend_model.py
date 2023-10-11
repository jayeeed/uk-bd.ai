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
    
def save_recommendations(user_id, search_params, recommended_property_ids):
    user_id_obj = ObjectId(user_id)  # Convert user_id to ObjectId
    
    # Exclude "_id" from the search parameters
    search_params.pop("_id", None)

    # Create a new search entry containing search parameters, recommended properties, and success
    search_entry = {
        "search_parameters": search_params,
        "recommended_properties": recommended_property_ids,
    }

    # Update the document for the user with the new search entry
    recommended_collection.update_one(
        {"_id": user_id_obj},
        {"$push": {"search_entries": search_entry}},
        upsert=True  # Create a new document if user_id_obj doesn't exist
    )
    
def save_success(_id, selected_property_id):
    success_id = ObjectId(_id)  # Convert user_id to ObjectId

    # Find the document for the user
    user_document = recommended_collection.find_one({"_id": success_id})

    if user_document:
        # If the user document exists, check if the "success" field already exists
        if "selected_properties" in user_document:
            # If it exists, fetch the existing "success" field as a list
            success_list = user_document["selected_properties"]
            # Append the new selected_property_id to the list
            success_list.append(selected_property_id)
            # Update the user document with the new "success" list
            recommended_collection.update_one(
                {"_id": success_id},
                {"$set": {"selected_properties": success_list}}
            )
        else:
            # If it doesn't exist, create a new list with the selected_property_id
            recommended_collection.update_one(
                {"_id": success_id},
                {"$set": {"selected_properties": [selected_property_id]}}
            )
    else:
        # If the user document doesn't exist, create a new document with the "success" field as a list
        recommended_collection.insert_one({"_id": success_id, "selected_properties": [selected_property_id]})
