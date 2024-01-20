import pandas as pd
from db.db_config import review_collection

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from bson import ObjectId

sia = SentimentIntensityAnalyzer()

def get_sentiment_label(sentence):
    sentiment = sia.polarity_scores(sentence)
    if sentiment['compound'] >= 0.05:
        return 'Positive'
    elif sentiment['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'



def data_clean(propertyId):
    
    # cursor = review_collection.find({"propertyId": propertyId })
    cursor = review_collection.find({"propertyId": ObjectId(propertyId)})
    documents_list = list(cursor)
    
    review_df = pd.DataFrame(documents_list)

    sentiment_column = review_df['sentiment']
    #print(sentiment_column)
    review_df['sentiment'].fillna('Neutral', inplace=True)
    #print(sentiment_column)

    sentiment_counts = review_df['sentiment'].value_counts()
    print(sentiment_counts)

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








    # for document in cursor:
    #     print(document)

    # Convert documents to a list of dictionaries

    # print(review_df)
    
    # print("DataFrame Structure:", review_df.info())
    # print("DataFrame Head:", review_df.head())