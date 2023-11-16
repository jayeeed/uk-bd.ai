from flask import Flask, request, jsonify, make_response
import pandas as pd
import numpy as np
from textblob import TextBlob
from sklearn.neighbors import NearestNeighbors
# from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import HistGradientBoostingRegressor
# from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
# from flask_cors import CORS, cross_origin
import joblib
from db.db_config import allProperties_collection

# app = Flask(__name__)

# CORS(app, resources={r"/add-properties": {"origins": "http://localhost:3009"}})

# Load the property data from MongoDB
# property_data = list(mongo.db.price.find())

property_data = list(allProperties_collection.find())



# df = pd.DataFrame(property_data)
# print(df)

data = pd.DataFrame(property_data)
# print(data)

# duplicates = df.apply(lambda x: x.duplicated()).sum()
# print(duplicates)
# data = df.drop_duplicates()

# print(data)

property_df = data.drop(columns=['_id', 'userId', 'title', 'images', 'description',
                        'decideReservations', 'discounts', 'status', 'createdAt', 'updatedAt', '__v'])
print(property_df)

# property_df.dropna(inplace=True)

property_df['lat'] = property_df['located'].apply(lambda x: x['lat'])
property_df['lon'] = property_df['located'].apply(lambda x: x['lon'])

google_locations = property_df[['lat', 'lon']].values
print(google_locations)

k = 3  # Number of neighbors to consider

num_samples = len(google_locations)

if num_samples >= k:

    # k = 5  # Number of neighbors to consider
    nn_model = NearestNeighbors(n_neighbors=k)
    nn_model.fit(google_locations)
    neighbors_indices = nn_model.kneighbors(
        google_locations, n_neighbors=k, return_distance=False)
    
    # Identify rows with non-numeric values in the "price" column
    non_numeric_rows = property_df[property_df["price"].isnull()]

    # Replace non-numeric values in the "price" column with a default value (e.g., 0)
    property_df["price"] = pd.to_numeric(property_df["price"], errors="coerce").fillna(0)
    print(non_numeric_rows)
    


    avg_neighbor_prices = []
    for indices in neighbors_indices:
        avg_price = property_df.loc[indices, "price"].mean()
        avg_neighbor_prices.append(avg_price)
    property_df["avg_neighbor_price"] = avg_neighbor_prices
    print(property_df["avg_neighbor_price"])
else:
    print("Not enough samples for k neighbors.")

# Extract values from 'guests' object and create new columns
property_df['bedrooms'] = property_df['guests'].apply(lambda x: x['bedrooms'])
property_df['beds'] = property_df['guests'].apply(lambda x: x['beds'])
property_df['bathrooms'] = property_df['guests'].apply(
    lambda x: x['bathrooms'])
property_df['guests'] = property_df['guests'].apply(lambda x: x['guests'])

numeric_features = ["bedrooms", "price", "bathrooms", "beds", "guests"]
print(numeric_features)

numeric_df = property_df[numeric_features].fillna(
    property_df[numeric_features].mean())
print(numeric_df)


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
print(categorical_features)

categorical_df = property_df[categorical_features].fillna(
    property_df[categorical_features].mode().iloc[0])
print(categorical_df)

label_encoder = LabelEncoder()
for feature in categorical_features:
    categorical_df[feature] = label_encoder.fit_transform(
        categorical_df[feature])
print(categorical_df[feature])

# Combine numeric and categorical DataFrames
combined_df = pd.concat([numeric_df, categorical_df], axis=1)
print(combined_df)

combined_df['price'] = pd.to_numeric(property_df['price'], errors='coerce')

# Remove extreme outliers in base_price
price_df = property_df[combined_df['price'] < 5000]
print(price_df)

# Transformation
combined_df['log_base_price'] = np.log(combined_df['price'])
print(combined_df['log_base_price'])


X = combined_df.drop(columns=["price", "log_base_price"])
y = combined_df["log_base_price"]
print(X)
print(y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)


scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ridge_model = Ridge()
# ridge_model.fit(X_train_scaled, y_train)


# y_pred = ridge_model.predict(X_test_scaled)
# print(y_pred)

HistGradientBoostingRegressor_model = HistGradientBoostingRegressor()
HistGradientBoostingRegressor_model.fit(X_train_scaled, y_train)
y_pred = HistGradientBoostingRegressor_model.predict(X_test_scaled)

mse = mean_squared_error(y_test, y_pred)
# print("Ridge Regression Model:", ridge_model)
# print("Ridge Regression Model:", y_pred)

print("Hist Gradient Boosting Regressor Model:", y_pred)
print("Mean Squared Error:", mse)


# Save the model to a file using joblib
# joblib.dump(ridge_model, 'ridge_model.joblib')


joblib.dump(HistGradientBoostingRegressor_model, 'price_prediction/ml_models/model.joblib')
joblib.dump(scaler, 'price_prediction/ml_models/scaler.joblib')

# Load the model from the file using joblib
# loaded_model = joblib.load('ridge_model.joblib')

loaded_model = joblib.load('price_prediction/ml_models/model.joblib')


# # @app.route('/predict', methods=['POST', 'OPTIONS'])
# @app.route('/price', methods=['POST', 'OPTIONS'])
# @cross_origin(origin="localhost", headers=["Content-Type", "authorization"])
# def handle_options():
#     if request.method == 'OPTIONS':
#         response = make_response()
#         response.headers.add("Access-Control-Allow-Origin", "*")
#         # response.headers.add("Access-Control-Allow-Origin", "http://localhost:3003")
#         response.headers.add("Access-Control-Allow-Headers", "Content-Type")
#         response.headers.add("Access-Control-Allow-Methods", "OPTIONS, POST")
#         return response

#     elif request.method == 'POST':
#         responseData = request.json
#         data = responseData.get('values', {})
#         print("Received data:", data)

#         placeDescribesId = data.get('placeDescibe')
#         typeOfPlaceId = data.get('typeOfPlace')
#         located = data.get('locatedPlace', {})
#         address = data.get('addAddress', {})
#         guests = data.get('guests', {})
#         amenitiesIds = data.get('offer', [])
#         images = data.get('uploadPhoto', [])
#         title = data.get('shortTitle')

#         suggested_price = get_pred(X_test_scaled)
#         print("suggested_price", suggested_price)
#         nearest_price = get_nearest(located)
#         print("nearest_price", nearest_price)
#         print("placeDescribesId", placeDescribesId)
#         print("typeOfPlaceId", typeOfPlaceId)
#         print("address", address)
#         print("title", title)

#     if title and placeDescribesId and typeOfPlaceId and located and address and guests and amenitiesIds and images and request.method == 'POST':
#         id = mongo.db.prediction.insert_one({
#             "shortTitle": title, "placeDescibe": placeDescribesId, "typeOfPlace": typeOfPlaceId,
#             "locatedPlace": located, "addAddress": address, "guests": guests, "offer": amenitiesIds, "uploadPhoto": images,
#             "suggested_price": suggested_price,
#             "nearest_price": nearest_price
#         })

#         resp = jsonify({'message': 'Suggested price successfully created!',
#                        "suggested_price": suggested_price, "nearest_price": nearest_price})
#         resp.status_code = 201  # Created status code
#         return resp

#     else:
#         resp = jsonify({'error': 'Invalid data or missing values'})
#         resp.status_code = 400  # Bad Request status code
#         return resp


# def get_pred(X_test_scaled):
#     suggested_price = model.predict(X_test_scaled)[0]
#     formatted_price = round(np.exp(suggested_price), 2)
#     return formatted_price


# def get_nearest(located):
#     latitude = located.get('lat')
#     longitude = located.get('lon')
#     if latitude is not None and longitude is not None:
#         latitude = float(latitude)
#         longitude = float(longitude)
#         location_data = np.array([[latitude, longitude]])
#         print(location_data)
#         imputer = SimpleImputer(strategy='median')
#         location_data = imputer.fit_transform(location_data)
#         k = 3
#         nn_model = NearestNeighbors(n_neighbors=k)
#         nn_model.fit(locations)
#         neighbors_indices = nn_model.kneighbors(
#             location_data, n_neighbors=k, return_distance=False)
#         print(neighbors_indices)
#         avg_neighbor_price = round(
#             property_df.loc[neighbors_indices[0], "price"].mean(), 2)
#         return avg_neighbor_price
#     else:
#         # Handle the case where 'lat' or 'lon' are None
#         return None


# if __name__ == '__main__':
#     app.run('localhost', 5001)
