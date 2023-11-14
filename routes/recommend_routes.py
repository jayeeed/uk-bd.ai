from flask import Blueprint, request, jsonify
from models.recommend_model import get_recommendations, save_recommendations, save_success
from flask_cors import CORS, cross_origin

search_properties_route = Blueprint('search_properties_route', __name__)

CORS(search_properties_route, resources={r"/api/search": {"origins": "http://localhost:3009"}})

@search_properties_route.route('/api/search', methods=['POST'])
def search_properties():
    data = request.json

    recommended_property_ids = get_recommendations(data)
    search_id = data.get("_id")
    save_recommendations(search_id, data, recommended_property_ids)

    return jsonify({"recommended_property_ids": recommended_property_ids})


@search_properties_route.route('/api/success', methods=['POST'])
def save_selected_property():
    data = request.json  # Assuming you're sending JSON data in the request
    
    save_id = data.get("_id")  # Assuming "_id" is sent in the JSON request
    selected_property_id = data.get("selected_property_id")
    
    save_success(save_id, selected_property_id)
    
    return jsonify({"selected_property_id": selected_property_id})

