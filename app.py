from flask import Flask
from routes.recommend_routes import search_properties_route
from routes.property_routes import property_routes
from routes.instant_varification_routes import verify_routes
from flask_cors import CORS

import os 

app = Flask(__name__, static_folder='../static')

CORS(app)

app.register_blueprint(search_properties_route)
app.register_blueprint(property_routes)
app.register_blueprint(verify_routes)



port = int(os.environ.get("PORT", 7050)) 

if __name__ == '__main__':
   
   app.run(debug=True, port=port, host='0.0.0.0')


# app = Flask(__name__, 
# template_folder='../templates',
# static_folder='../static')