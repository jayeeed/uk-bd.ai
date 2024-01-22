from dotenv import load_dotenv
from flask import Blueprint, request, jsonify,make_response
from flask_cors import CORS ,cross_origin
import numpy as np
from textblob import TextBlob
from sklearn.impute import SimpleImputer
from sklearn.neighbors import NearestNeighbors
from db.db_config import price_prediction, description_collection
from features.price_prediction.price import X_test_scaled,HistGradientBoostingRegressor_model,google_locations,property_df

price_predict_routes = Blueprint('price_predict_routes', __name__)


import os
load_dotenv()

CORS_ORIGIN = os.getenv('CORS_ORIGIN')

print(type(CORS_ORIGIN))


# CORS(price_predict_routes, resources={r"/api/price/*": {"origins": "http://localhost:3009/add-properties"}})

CORS(price_predict_routes, resources={
    r"/api/price": {"origins": CORS_ORIGIN},
    r"/api/description": {"origins": "http://localhost:3009/add-properties"}})


# CORS(price_predict_routes, resources={})


# @app.route('/predict', methods=['POST', 'OPTIONS'])
# @cross_origin(origin="localhost", headers=["Content-Type", "authorization"])
@price_predict_routes.route('/api/price', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def handle_price_options():
    """
    This function handles the price prediction request.
    It receives the necessary data from the request body, predicts the price using a machine learning model,
    finds the nearest price based on location, and inserts the data into a database. If all required data is present,
    a success message with the predicted price and nearest price is returned, otherwise an error message is returned.
    """
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        # response.headers.add("Access-Control-Allow-Origin", "http://localhost:3003")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "OPTIONS, POST")
        return response

    elif request.method == 'POST':
        responseData = request.json
        data = responseData.get('values', {})
        # print("Received data:", data)

        placeDescribesId = data.get('placeDescibe')
        typeOfPlaceId = data.get('typeOfPlace')
        located = data.get('locatedPlace', {})
        address = data.get('addAddress', {})
        guests = data.get('guests', {})
        amenitiesIds = data.get('offer', [])
        images = data.get('uploadPhoto', [])
        title = data.get('shortTitle')

        suggested_price = get_pred(X_test_scaled)
        # print("suggested_price", suggested_price)
        nearest_price = get_nearest(located)
        # print("nearest_price", nearest_price)
        # print("placeDescribesId", placeDescribesId)
        # print("typeOfPlaceId", typeOfPlaceId)
        # print("address", address)
        # print("title", title)

    if title and placeDescribesId and typeOfPlaceId and located and address and guests and amenitiesIds and images and request.method == 'POST':
        id = price_prediction.insert_one({  
            "shortTitle": title, "placeDescibe": placeDescribesId, "typeOfPlace": typeOfPlaceId,
            "locatedPlace": located, "addAddress": address, "guests": guests, "offer": amenitiesIds, "uploadPhoto": images,
            "suggested_price": suggested_price,
            "nearest_price": nearest_price
        })

        resp = jsonify({'message': 'Suggested price successfully created!',
                       "suggested_price": suggested_price, "nearest_price": nearest_price})
        resp.status_code = 201  # Created status code
        return resp

    else:
        resp = jsonify({'error': 'Invalid data or missing vmake_responsealues'})
        resp.status_code = 400  # Bad Request status code
        return resp

def get_pred(X_test_scaled):
    suggested_price = HistGradientBoostingRegressor_model.predict(X_test_scaled)[0]
    formatted_price = round(np.exp(suggested_price), 2)
    return formatted_price

def get_nearest(located):
    latitude = located.get('lat')
    longitude = located.get('lon')
    if latitude is not None and longitude is not None:
        latitude = float(latitude)
        longitude = float(longitude)
        location_data = np.array([[latitude, longitude]])
        # print(location_data)
        imputer = SimpleImputer(strategy='median')
        location_data = imputer.fit_transform(location_data)
        k = 3
        nn_model = NearestNeighbors(n_neighbors=k)
        nn_model.fit(google_locations)
        neighbors_indices = nn_model.kneighbors(
            location_data, n_neighbors=k, return_distance=False)
        # print(neighbors_indices)
        avg_neighbor_price = round(
            property_df.loc[neighbors_indices[0], "price"].mean(), 2)
        return avg_neighbor_price
    else:
        # Handle the case where 'lat' or 'lon' are None
        return None


# @cross_origin(origin="localhost", headers=["Content-Type", "authorization"])
@price_predict_routes.route('/api/description', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def handle_description_options():
    """
    This function handles the description request.
    It receives the description from the request body, predicts the sentiment and emotion using machine learning models,
    and inserts the data into a database. If all required data is present, a success message with the predicted sentiment and emotion is returned, otherwise an error message is returned.
    """
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        # response.headers.add("Access-Control-Allow-Origin", "http://localhost:3003")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "OPTIONS, POST")
        return response

    elif request.method == 'POST':

        data = request.json
        # print("Received data:", data)
        description = data.get('text')

        sentiment = get_predict(description)
        # print(sentiment)
        # print("description", description)
        emotion = get_emotion_from_text(description)
        # print(emotion)

    if description and request.method == 'POST':
        id = description_collection.insert_one({  
            "description": description,
            "sentiment": sentiment,
            "emotion": emotion
        })
        resp = jsonify({'message': 'Emotion and sentiment successfully created!',
                       "sentiment": sentiment, "emotion": emotion})
        resp.status_code = 201  # Created status code
        return resp

    else:
        resp = jsonify({'error': 'Invalid data or missing values'})
        resp.status_code = 400  # Bad Request status code
        return resp


def get_predict(description):
    """
    This function uses the VADER sentiment analysis algorithm to extract emotions from a given text.
    It returns a dictionary containing the emotions and their scores.
    """
    if description is not None and isinstance(description, str):
        sentiment_polarity = TextBlob(description).sentiment.polarity

        # Classify the sentiment based on the sentiment score
        if sentiment_polarity >= 0.05:
            return 'positive'
        elif sentiment_polarity <= -0.05:
            return 'negative'
        else:
            return 'neutral'


def get_emotion_from_text(description):
    """
    This function uses a simple heuristic to extract emotions from a given text.
    It returns a string representing the emotion, or 'neutral' if no emotion is detected.
    """
    if description is not None and isinstance(description, str):
        blob = TextBlob(description)
        polarity = blob.sentiment.polarity
        if "fear" in description.lower() or "anxious" in description.lower() or "nervous" in description.lower():
            return "fear"
        elif "surprised" in description.lower() or "shocked" in description.lower() or "amazed" in description.lower():
            return "surprise"
        elif polarity > 0.2:
            return "happiness"
        elif polarity < -0.2:
            return "sadness"
        elif polarity < 0 and polarity >= -0.2:
            return "anger"
        else:
            return "neutral"
    else:
        return 'neutral'












# CORS(app, resources={r"/add-properties": {"origins": CORS_ORIGIN}})

# property_data = list(mongo.db.allproperties.find())

# data = pd.DataFrame(property_data)

# property_df = data.drop(columns=['_id', 'userId', 'title', 'placeDescribesId', 'typeOfPlaceId', 'images', 'located', 'guests', 'price',
#                         'amenitiesIds', 'address', 'decideReservations', 'discounts', 'status', 'createdAt', 'updatedAt', '__v'])
# print(property_df)

# # Extract the reviews from the DataFrame
# reviews = np.array(property_df['description'])
# test_reviews = reviews[::]
# sample_review_ids = []
# test_reviews = np.array(test_reviews)

# for sample_review_id in sample_review_ids:
#     description = test_reviews[sample_review_id]
#     print('REVIEW:', description)
#     print('Predicted Sentiment polarity:',
#           TextBlob(description).sentiment.polarity)
#     print('-' * 60)

# # Calculate sentiment polarity for all test reviews
# sentiment_polarity = [
#     TextBlob(review).sentiment.polarity for review in test_reviews]
# print(sentiment_polarity)

