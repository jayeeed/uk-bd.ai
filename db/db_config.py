from pymongo import MongoClient
import pandas as pd

client = MongoClient(
    'mongodb+srv://ipsita:Ipsita%402023@uk-bd0.u3pngqk.mongodb.net/')

db = client['airbnb']
properties_collection = db['allproperties']
recommended_collection = db['recommended_properties']
bookings_collection = db['bookings']
sentiment_reviews_collection = db['sentiment_reviews']
FAQ_ans_corpus = db['ans_corpus']


def get_data():
    data_from_mongodb = properties_collection.find()
    data_df = pd.DataFrame(data_from_mongodb)
    return data_df


def insert_sentiment_data(sentence, sentiment_label):
    post = {"sentence": sentence, "sentiment": sentiment_label}
    post_id = sentiment_reviews_collection.insert_one(post).inserted_id
    return post_id
