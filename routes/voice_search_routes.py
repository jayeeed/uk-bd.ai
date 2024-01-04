from db.db_config import properties_collection
from features.voice_search.utils import utils
from flask import Blueprint, request, jsonify
from bson import json_util, ObjectId
import json
from flask_cors import CORS, cross_origin

voice_search_routes = Blueprint('voice_search_routes', __name__)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

voice_search_routes.json_encoder = CustomJSONEncoder

# from flask_cors import CORS
CORS(voice_search_routes, resources={r"/api": {"origins": "http://localhost:3009"}})





@voice_search_routes.route("/api/search", methods=['GET'])
@cross_origin(supports_credentials=True)
def search_autocomplete():
    try:
        query = request.args.get("searchText", "").lower()
        tokens = query.split(" ")
    
        response_data = utils.voice_search(tokens)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
       # response_data = json.loads(result_json)
        
    return jsonify(response_data)

