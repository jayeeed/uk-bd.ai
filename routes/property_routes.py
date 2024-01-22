from dotenv import load_dotenv
from db.db_config import properties_collection
from flask import Blueprint, request, jsonify

from flask_cors import CORS

property_routes = Blueprint('property_routes', __name__)


import os
load_dotenv()

CORS_ORIGIN = os.getenv('CORS_ORIGIN')

print(type(CORS_ORIGIN))

# from flask_cors import CORS

CORS(property_routes, resources={r"api/property/list/*": {"origins": CORS_ORIGIN}})


@property_routes.route('/api/property/<property_id>', methods=['GET'])
def get_property_details(property_id):
    property_data = properties_collection.find_one({"property_id": int(property_id)})
    
    if property_data:
        # Convert ObjectId to a string for JSON serialization
        property_data['_id'] = str(property_data['_id'])
        
        return jsonify(property_data)
    else:
        return jsonify({"message": "Property not found"}), 404
