from flask import Blueprint, jsonify
from bson import ObjectId  # Import ObjectId from bson module
from db.db_config import properties_collection

property_routes = Blueprint('property_routes', __name__)

# from flask_cors import CORS

# CORS(search_properties_route, resources={r"/api/recommended/*": {"origins": "http://localhost:3009"}})

@property_routes.route('/api/property/<property_id>', methods=['GET'])
def get_property_details(property_id):
    property_data = properties_collection.find_one({"property_id": int(property_id)})
    
    if property_data:
        # Convert ObjectId to a string for JSON serialization
        property_data['_id'] = str(property_data['_id'])
        
        return jsonify(property_data)
    else:
        return jsonify({"message": "Property not found"}), 404