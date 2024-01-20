from db.db_config import review_collection
from flask import Blueprint, request, jsonify


from flask_cors import CORS

from features.review_analysis.utils.get_sentiment import get_sentiment_label, data_clean

review_sentiment_routes = Blueprint('review_sentiment_routes', __name__)

# from flask_cors import CORS

CORS(review_sentiment_routes, resources={r"/api/*": {"origins": "http://localhost:3009"}})

@review_sentiment_routes.route('/api/insert_sentiment', methods=['POST'])
def insert_sentiment():
    if request.method == 'POST':
        if request.headers.get('content-type') == 'application/json':
            json_data = request.get_json()
            reviewMessage = json_data.get('reviewMessage')
            propertyId = json_data.get('propertyId')
            reviewedBy = json_data.get('reviewedBy')
            print(propertyId)
        
        sentiment_label = get_sentiment_label(reviewMessage)
            
            # property_id_to_find = {
            #     "propertyId": ObjectId(propertyId),
            #     "reviewedBy": ObjectId(reviewedBy)
            # }

            # Finding the relevant document
        document_to_update = review_collection.find_one({
                "propertyId": propertyId , "reviewedBy":reviewedBy})


        if document_to_update:
                #print(document_to_update)
                # Update the document with sentiment_label
                review_collection.update_one(
                    {"_id": document_to_update["_id"]},  # Use _id for updating
                    # {"_id": ObjectId("657ead0acb652787604f8881")}, 
                    {"$set": {"sentiment": sentiment_label ,
                              "reviewMessage": reviewMessage}}
                )
                response_data = {
                    "sentence": reviewMessage,
                    "result": "Document updated successfully",
                    "sentiment": sentiment_label
                }
        else:
                response_data = {
                    "sentence": reviewMessage,
                    "result": "Document not found for the given propertyId and reviewedBy",
                    "sentiment": sentiment_label
                }
        
        return jsonify(response_data)
    
    return jsonify({"error": "Only POST requests are supported on this endpoint."})




@review_sentiment_routes.route('/api/get_review_sentiment', methods=['POST'])
def get_review_sentiment():
    if request.method == 'POST':
        # Check if request content-type is JSON
        if request.headers.get('content-type') == 'application/json':
            json_data = request.get_json()
            propertyId = json_data.get('propertyId')
        else:
            propertyId = request.form.get('propertyId')
            
        print(propertyId)
        
        positive_percentage, negative_percentage = data_clean(propertyId)
        
        response = {
        "Positive": f"{positive_percentage:.2f}%",
        "Negative": f"{negative_percentage:.2f}%"
    }
        return jsonify(response)
    
    return jsonify({"error": "Only POST requests are supported on this endpoint."})

