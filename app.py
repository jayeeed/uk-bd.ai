from flask import Flask
from routes.recommend_routes import search_properties_route
from routes.price_prediction_routes import price_predict_routes
from routes.property_routes import property_routes
from routes.instant_varification_routes import verify_routes
from routes.chat_bot_routes import chatBot_routes
from flask_cors import CORS

import os 

app = Flask(__name__, static_folder='../static')

# CORS(app, resources={r"/add-properties": {"origins": "http://localhost:3009"},
#                      r"/e-check": {"origins": "http://localhost:3009"}})

CORS(app)

app.register_blueprint(chatBot_routes)
app.register_blueprint(search_properties_route)
app.register_blueprint(property_routes)
app.register_blueprint(price_predict_routes)
app.register_blueprint(verify_routes)






port = int(os.environ.get("PORT", 7050)) 

if __name__ == '__main__':
   app.run(debug=True, port=port, host='0.0.0.0')


# app = Flask(__name__, 
# template_folder='../templates',
# static_folder='../static')



# from flask import Flask
# from flask_pymongo import PyMongo
# from flask_cors import CORS, cross_origin

# app = Flask(__name__)
# app.secret_key = "secret key"
# app.config["MONGO_URI"] = "mongodb+srv://ipsita:Ipsita%402023@uk-bd0.u3pngqk.mongodb.net/airbnb"
# # app.config["MONGO_URI"] = "mongodb://localhost:27017/price_prediction"
# app.config["CORS_HEADERS"] = "Content-Type"
# mongo = PyMongo(app)
