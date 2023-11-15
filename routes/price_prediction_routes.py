from flask import Flask, request, jsonify, make_response
import pandas as pd
import numpy as np
from textblob import TextBlob
from flask_cors import CORS, cross_origin
from app import mongo

price_prediction_routes = Blueprint('price_prediction_routes', __name__)

@property_routes.route('/api/property/<property_id>', methods=['GET'])
def get_property_details(property_id):
    property_data = properties_collection.find_one({"property_id": int(property_id)})
    
    if property_data:
        # Convert ObjectId to a string for JSON serialization
        property_data['_id'] = str(property_data['_id'])
        
        return jsonify(property_data)
    else:
        return jsonify({"message": "Property not found"}), 404


CORS(app, resources={r"/add-properties": {"origins": "http://localhost:3009"}})

property_data = list(mongo.db.allproperties.find())

data = pd.DataFrame(property_data)

property_df = data.drop(columns=['_id', 'userId', 'title', 'placeDescribesId', 'typeOfPlaceId', 'images', 'located', 'guests', 'price',
                        'amenitiesIds', 'address', 'decideReservations', 'discounts', 'status', 'createdAt', 'updatedAt', '__v'])
print(property_df)

# Extract the reviews from the DataFrame
reviews = np.array(property_df['description'])
test_reviews = reviews[::]
sample_review_ids = []
test_reviews = np.array(test_reviews)

for sample_review_id in sample_review_ids:
    description = test_reviews[sample_review_id]
    print('REVIEW:', description)
    print('Predicted Sentiment polarity:',
          TextBlob(description).sentiment.polarity)
    print('-' * 60)

# Calculate sentiment polarity for all test reviews
sentiment_polarity = [
    TextBlob(review).sentiment.polarity for review in test_reviews]
print(sentiment_polarity)


@price_prediction_routes.route('/description', methods=['POST', 'OPTIONS'])
@cross_origin(origin="localhost", headers=["Content-Type", "authorization"])
def handle_options():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        # response.headers.add("Access-Control-Allow-Origin", "http://localhost:3003")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "OPTIONS, POST")
        return response

    elif request.method == 'POST':

        data = request.json
        print("Received data:", data)
        description = data.get('text')

        sentiment = get_predict(description)
        print(sentiment)
        print("description", description)
        emotion = get_emotion_from_text(description)
        print(emotion)

    if description and request.method == 'POST':
        id = mongo.db.description.insert_one({
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


if __name__ == '__main__':
    app.run('localhost', 5002)
