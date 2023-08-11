from flask import Blueprint, request, jsonify
from models.recommend_model import get_recommendations, save_recommendations

search_properties_route = Blueprint('search_properties_route', __name__)

@search_properties_route.route('/api/search', methods=['POST'])
def search_properties():
    data = request.json  # Assuming you're sending JSON data in the request

    recommended_property_ids = get_recommendations(data)
    
    user_id = data.get("user_id")  # Assuming user_id is sent in the JSON request
    save_recommendations(user_id, data, recommended_property_ids)

    return jsonify({"recommended_property_ids": recommended_property_ids})

