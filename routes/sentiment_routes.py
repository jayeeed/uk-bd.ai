from flask import Blueprint, request, jsonify
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from db.db_config import insert_sentiment_data

sentiment_route = Blueprint('sentiment_route', __name__)

sia = SentimentIntensityAnalyzer()

def get_sentiment_label(sentence):
    sentiment = sia.polarity_scores(sentence)
    if sentiment['compound'] >= 0.05:
        return 'Positive'
    elif sentiment['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

@sentiment_route.route('/sentiment', methods=['POST'])
def index():
    if request.method == 'POST':
        # Check if request content-type is JSON
        if request.headers.get('content-type') == 'application/json':
            json_data = request.get_json()
            sentence = json_data.get('sentence')
        else:
            sentence = request.form.get('sentence')

        sentiment_label = get_sentiment_label(sentence)
        post_id = insert_sentiment_data(sentence, sentiment_label)

        response_data = {
            "sentence": sentence,
            "sentiment": sentiment_label,
            "post_id": str(post_id)
        }
        return jsonify(response_data)

    return jsonify({"error": "Only POST requests are supported on this endpoint."})
