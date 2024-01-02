from flask import Flask, render_template, request, jsonify
import pymongo
from pymongo import MongoClient
from nltk.sentiment.vader import SentimentIntensityAnalyzer

app = Flask(__name__)

sia = SentimentIntensityAnalyzer()

def get_sentiment_label(sentence):
    sentiment = sia.polarity_scores(sentence)
    if sentiment['compound'] >= 0.05:
        return 'Positive'
    elif sentiment['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        # Check if request content-type is JSON
        if request.headers.get('content-type') == 'application/json':
            json_data = request.get_json()
            sentence = json_data.get('sentence')
        else:
            sentence = request.form.get('sentence')
        
        sentiment_label = get_sentiment_label(sentence)
        
        with pymongo.MongoClient('mongodb://localhost:27017/') as client:
            db = client['sentiment']
            collection = db['data']
            post = {"sentence": sentence, "sentiment": sentiment_label}
            post_id = collection.insert_one(post).inserted_id
        
        response_data = {
            "sentence": sentence,
            "sentiment": sentiment_label
        }
        return jsonify(response_data)
    
    return jsonify({"error": "Only POST requests are supported on this endpoint."})

if __name__ == '__main__':
    app.run(debug=True)
