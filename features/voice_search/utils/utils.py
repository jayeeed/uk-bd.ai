from bson import json_util, ObjectId
import json
from db.db_config import properties_collection

 
def voice_search(tokens):
    # try:
    #     query = request.args.get("searchText", "").lower()
    #     tokens = query.split(" ")

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
        cursor = properties_collection.find(payload).limit(10)

        result_list = list(cursor)
        result_json = json_util.dumps(result_list, default=json_util.default)
        response_data = json.loads(result_json)

        return response_data

    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500




# class CustomJSONEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, ObjectId):
#             return str(obj)
#         return super().default(obj)


# app = Flask(__name__)
# app.json_encoder = CustomJSONEncoder # type: ignore
# CORS(app)


# Connect to MongoDB
# client = MongoClient(
#     'mongodb+srv://ipsita:Ipsita%402023@uk-bd0.u3pngqk.mongodb.net/airbnb')
# db = client['airbnb']
# collection = db['allproperties']
