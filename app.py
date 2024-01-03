from flask import Flask
from routes.sentiment_routes import sentiment_route
from routes.voice_search_routes import voice_search_route
from routes.recommend_routes import search_properties_route
from routes.property_routes import property_routes
# from routes.price_prediction_routes import price_predict_routes
# from routes.instant_varification_routes import verify_routes
from routes.FAQ_chat import FAQ_chat_route

app = Flask(__name__)

app.register_blueprint(search_properties_route)
app.register_blueprint(property_routes)
# app.register_blueprint(price_predict_routes)
# app.register_blueprint(verify_routes)
app.register_blueprint(voice_search_route)
app.register_blueprint(sentiment_route)
app.register_blueprint(FAQ_chat_route)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
