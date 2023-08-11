from sklearn.preprocessing import OneHotEncoder
from sklearn.neighbors import NearestNeighbors
import pandas as pd
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
    data_df = get_data()  # Retrieve data from the database, e.g., properties_collection.find()

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
    recommended_collection.insert_one({
        "user_id": user_id,
        "search_parameters": {key: value for key, value in search_params.items() if key != "user_id"},
        "recommended_properties": recommended_property_ids
    })

