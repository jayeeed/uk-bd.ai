from flask import Flask
from routes.recommend_routes import search_properties_route

app = Flask(__name__)

app.register_blueprint(search_properties_route)

if __name__ == '__main__':
    app.run(debug=True)
