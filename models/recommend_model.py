from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors
import pandas as pd
from tqdm import tqdm
from bson import ObjectId
from db.db_config import get_data, recommended_collection, bookings_collection

def preprocess_data(data_df):
    
    ##################################################################

    property_df = data_df.drop(columns=['_id', 'userId', 'title', 'images', 'description',
                            'decideReservations', 'discounts', 'status', 'createdAt', 'updatedAt', '__v'])

    # property_df.dropna(inplace=True)
    # property_df['lat'] = property_df['located'].apply(lambda x: x['lat'])
    # property_df['lon'] = property_df['located'].apply(lambda x: x['lon'])
    # locations = property_df[['lat', 'lon']].values

    # Extract values from 'guests' object and create new columns
    property_df['bedrooms'] = property_df['guests'].apply(lambda x: x['bedrooms'])
    property_df['beds'] = property_df['guests'].apply(lambda x: x['beds'])
    property_df['bathrooms'] = property_df['guests'].apply(
        lambda x: x['bathrooms'])
    property_df['guests'] = property_df['guests'].apply(lambda x: x['guests'])

    numeric_features = ["bedrooms", "price", "bathrooms", "beds", "guests"]
    numeric_df = property_df[numeric_features]

    # Function to expand the 'amenitiesIds' array into separate columns
    def expand_amenities(row):
        amenities = row['amenitiesIds']
        expanded_amenities = {}
        for i in range(len(amenities)):
            column_name = f'amenitiesIds[{i}]'
            expanded_amenities[column_name] = amenities[i]
        return pd.Series(expanded_amenities)

    # Apply the expansion function to each row and concatenate the result
    expanded_amenities_df = property_df.apply(expand_amenities, axis=1)

    # Merge the expanded amenities DataFrame with the original DataFrame
    property_df = pd.concat([property_df, expanded_amenities_df], axis=1)

    # Function to expand the 'address' object into separate columns
    def expand_address(row):
        address_data = row['address']
        expanded_address = {}
        for key, value in address_data.items():
            column_name = f'address.{key}'
            expanded_address[column_name] = value
        return pd.Series(expanded_address)

    # Apply the expansion function to each row and concatenate the result
    expanded_address_df = property_df.apply(expand_address, axis=1)

    # Merge the expanded address DataFrame with the original DataFrame
    property_df = pd.concat([property_df, expanded_address_df], axis=1)

    # Define categorical features
    categorical_features = ['placeDescribesId', 'typeOfPlaceId'] + \
        list(expanded_amenities_df.columns) + list(expanded_address_df.columns)

    categorical_df = property_df[categorical_features].fillna(
        property_df[categorical_features].mode().iloc[0])

    label_encoder = LabelEncoder()
    for feature in categorical_features:
        categorical_df[feature] = label_encoder.fit_transform(
            categorical_df[feature])

    # Combine numeric and categorical DataFrames
    all_features = pd.concat([numeric_df, categorical_df], axis=1)
    
    return all_features

def train_model(all_features, batch_size=32):
    model = NearestNeighbors(n_neighbors=5, metric='euclidean')
    
    # Calculate the number of batches
    num_batches = len(all_features) // batch_size
    
    # Wrap the training loop with tqdm for a progress bar
    with tqdm(total=len(all_features), desc="Training") as pbar:
        for i in range(0, len(all_features), batch_size):
            batch = all_features[i:i+batch_size]
            model.fit(batch)
            
            # Update the progress bar after each batch
            pbar.update(min(batch_size, len(all_features) - i))
    
    return model
    
# Assuming this function is in your_module
def get_recommendations(renter_user_id):
    # Fetching previous booking data for the renter
    previous_bookings = bookings_collection.find({"renterUserId": ObjectId(renter_user_id)})

    # Extracting property IDs from previous bookings
    booked_property_ids = [str(booking["propertyId"]) for booking in previous_bookings]

    # Fetching all data
    data_df = get_data()

    # Filtering out properties that the renter has booked before
    data_df = data_df[~data_df["_id"].isin(booked_property_ids)]

    all_features = preprocess_data(data_df)
    model = train_model(all_features)

    # Getting recommendations for the renter
    _, indices = model.kneighbors()

    # Showing top 4 recommended properties that the renter has not booked before
    recommended_property_ids = [str(data_df.iloc[index]["_id"]) for index in indices[0][1:5]]

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
        # If the user document exists, check if the "selected_properties" field already exists
        if "selected_properties" in user_document:
            # If it exists, fetch the existing "selected_properties" field as a list
            success_list = user_document["selected_properties"]
            # Append the new selected_property_id to the list
            success_list.append(selected_property_id)
            # Update the user document with the new "selected_properties" list
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
        # If the user document doesn't exist, create a new document with the "selected_properties" field as a list
        recommended_collection.insert_one({"_id": success_id, "selected_properties": [selected_property_id]})
