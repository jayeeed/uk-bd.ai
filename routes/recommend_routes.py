from dotenv import load_dotenv
from features.recommend_properties.ml_models.recommend_model import get_recommendations, save_success
from flask import Blueprint, request, jsonify
from flask_cors import CORS

recommeded_properties_route = Blueprint('recommeded_properties_route', __name__)


import os
load_dotenv()

CORS_ORIGIN = os.getenv('CORS_ORIGIN')

print(type(CORS_ORIGIN))


CORS(recommeded_properties_route, resources={r"/api/recommended/*": {"origins": CORS_ORIGIN}})

@recommeded_properties_route.route('/api/recommended/<string:renter_user_id>', methods=['GET'])
def recommended_properties(renter_user_id):
    """
    This function returns a list of recommended properties based on the renter user ID.
    It returns a list of dictionaries representing the properties.
    """
    try:
        recommended_properties = get_recommendations(renter_user_id)
        return jsonify({"recommended_properties": recommended_properties})
    except Exception as e:
        # Log the exception for debugging
        print(f"Error in recommended_properties endpoint: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@recommeded_properties_route.route('/api/save', methods=['POST'])
def save_selected_property():
    """
    This function saves the selected property ID for a specific save ID.
    It returns None.
    """
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
