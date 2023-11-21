from flask import Flask
from routes.recommend_routes import search_properties_route
from routes.property_routes import property_routes
from routes.recommend_routes import search_properties_route
from routes.price_prediction_routes import price_predict_routes
from routes.property_routes import property_routes
from routes.instant_varification_routes import verify_routes

app = Flask(__name__)

app.register_blueprint(search_properties_route)
app.register_blueprint(property_routes)
app.register_blueprint(price_predict_routes)
app.register_blueprint(verify_routes)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=7050)
