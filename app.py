from flask import Flask
from routes.recommend_routes import search_properties_route
from routes.property_routes import property_routes
# from flask_cors import CORS, cross_origin

app = Flask(__name__)

# CORS(app, resources={r"/add-properties": {"origins": "http://localhost:3009"}})

app.register_blueprint(search_properties_route)
app.register_blueprint(property_routes)

if __name__ == '__main__':
    app.run(debug=True)
