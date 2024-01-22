import nltk
import os

nltk_data_path = 'nltk_data'

# Check if NLTK data exists at the specified path
if not os.path.exists(nltk_data_path):
    print("NLTK data not found. Downloading...")
    
    # Download NLTK data
    nltk.download("vader_lexicon",download_dir=nltk_data_path)
    
    print("Download complete.")

nltk.data.path.append("/nltk_data")


from flask import Flask
from routes.recommend_routes import recommeded_properties_route
from routes.property_routes import property_routes
from routes.review_sentiment_routes import review_sentiment_routes
from routes.price_prediction_routes import price_predict_routes
from routes.property_routes import property_routes
from routes.instant_varification_routes import verify_routes
from routes.voice_search_routes import voice_search_routes

# from routes.faq_chat_routes import faq_chat_route


app = Flask(__name__)

app.register_blueprint(recommeded_properties_route)
app.register_blueprint(review_sentiment_routes)
app.register_blueprint(voice_search_routes)
app.register_blueprint(property_routes)
app.register_blueprint(price_predict_routes)
app.register_blueprint(verify_routes)
# app.register_blueprint(faq_chat_route)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7050)
