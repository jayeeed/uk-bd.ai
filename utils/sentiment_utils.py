import pandas as pd
from db.db_config import sentiment_collection
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import nltk
nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

def get_sentiment_label(sentence):
    sentiment = sia.polarity_scores(sentence)
    if sentiment['compound'] >= 0.05:
        return 'Positive'
    elif sentiment['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

def data_clean():
    cursor = sentiment_collection.find({})
    # Convert documents to a list of dictionaries
    documents_list = list(cursor)
    review_df = pd.DataFrame(documents_list)
    #print(review_df)

    sentiment_column = review_df['sentiment']
    #print(sentiment_column)
    review_df['sentiment'].fillna('Neutral', inplace=True)
    print(sentiment_column)

    # Assuming your DataFrame is named review_df

    sentiment_counts = review_df['sentiment'].value_counts()

    positive_count = sentiment_counts.get('Positive', 0)
    negative_count = sentiment_counts.get('Negative', 0)

    total_positive_negative = positive_count + negative_count
    total_rows = len(review_df)

    if total_positive_negative > 0:
        positive_percentage = (positive_count / total_positive_negative) * 100
        negative_percentage = (negative_count / total_positive_negative) * 100
        print(f"Positive Percentage: {positive_percentage:.2f}%")
        print(f"Negative Percentage: {negative_percentage:.2f}%")
    else:
        print("No 'Positive' or 'Negative' sentiments found.")

    return positive_percentage, negative_percentage




# #@app.route('/', methods=['POST'])
# #def index():
#     if request.method == 'POST':
#         # Check if request content-type is JSON
#         if request.headers.get('content-type') == 'application/json':
#             json_data = request.get_json()
#             sentence = json_data.get('sentence')
#         else:
#             sentence = request.form.get('sentence')
        
#         sentiment_label = get_sentiment_label(sentence)
        
#         with pymongo.MongoClient('mongodb+srv://ipsita:Ipsita%402023@uk-bd0.u3pngqk.mongodb.net/') as client:
#             db = client['airbnb']
#             if db !="None":
#                 print('connected')
#             find_query = "find by Property ID then update the entity with sentiment field"
#             collection = db['reviews']
#             post = {"sentence": sentence, "sentiment": sentiment_label}
#             post_id = collection.insert_one(post).inserted_id
#             collection.update_one({"property_id": property_id_to_update}, {"$set": {"sentiment": sentiment_label}})
        
#         response_data = {
#             "sentence": sentence,
#             "sentiment": sentiment_label
#         }
#         return jsonify(response_data)
    
#     return jsonify({"error": "Only POST requests are supported on this endpoint."})
