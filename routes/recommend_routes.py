from flask import Blueprint, request, jsonify
from models.recommend_model import get_recommendations, save_recommendations, save_success
from flask_cors import CORS, cross_origin
from bson import ObjectId

search_properties_route = Blueprint('search_properties_route', __name__)

# CORS(search_properties_route, resources={r"/api/recommended/*": {"origins": "http://localhost:3009"}})

@search_properties_route.route('/api/recommended/<string:renter_user_id>', methods=['GET'])
def recommended_properties(renter_user_id):
    try:
        recommended_properties = get_recommendations(renter_user_id)
        return jsonify({"recommended_properties": recommended_properties})
    except Exception as e:
        # Log the exception for debugging
        print(f"Error in recommended_properties endpoint: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@search_properties_route.route('/api/save', methods=['POST'])
def save_selected_property():
    try:
        data = request.json  # Assuming you're sending JSON data in the request
        
        save_id = data.get("_id")  # Assuming "_id" is sent in the JSON request
        selected_property_id = data.get("selected_property_id")

        if not save_id or not selected_property_id:
            return jsonify({"error": "Invalid input data"}), 400

        save_success(save_id, selected_property_id)

        return jsonify({"selected_property_id": selected_property_id})
    except Exception as e:
        # Log the exception for debugging
        print(f"Error in save_selected_property endpoint: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
