from flask import Flask
from routes.recommend_routes import search_properties_route
from routes.property_routes import property_routes

app = Flask(__name__)

CORS(app)

app.register_blueprint(search_properties_route)
app.register_blueprint(property_routes)
app.register_blueprint(price_predict_routes)
app.register_blueprint(verify_routes)



if __name__ == '__main__':
    app.run(debug=True)
