from flask import Blueprint, Flask, request, jsonify
from flask_cors import CORS
from bson import json_util, ObjectId
import json
from db.db_config import get_data

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

voice_search_route = Blueprint('voice_search_route', __name__)

# CORS(voice_search_route, resources={r"/api/recommended/*": {"origins": "http://localhost:3009"}})

@voice_search_route.route("/search", methods=['GET'])
def search_autocomplete():
    try:
        query = request.args.get("searchText", "").lower()
        tokens = query.split(" ")

        clauses = [
            {
                "$or": [
                    {"title": {"$regex": token, "$options": "i"}},
                    {"description": {"$regex": token, "$options": "i"}},
                    {"located.display_name": {"$regex": token, "$options": "i"}},
                    {"located.address.country": {"$regex": token, "$options": "i"}},
                    {"address.country": {"$regex": token, "$options": "i"}},
                    {"address.city": {"$regex": token, "$options": "i"}},
                    {"address.state": {"$regex": token, "$options": "i"}}
                ]
            }
            for token in tokens
        ]
        payload = {"$and": clauses}
        cursor = get_data.find(payload).limit(10)

        result_list = list(cursor)
        result_json = json_util.dumps(result_list, default=json_util.default)
        response_data = json.loads(result_json)

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500