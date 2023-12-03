# "nid": regex_data['nid'],
# "dob": regex_data['dob']
from flask import jsonify
from bson.objectid import ObjectId
from db.db_config import db, user_collection

def update_collection(user_id, regex_data):

    # print(user_id)
    existing_user = user_collection.find_one({"_id": ObjectId(user_id)})
    # print(existing_user['email'])

    if not existing_user:
        return jsonify({"error": "User not found"}, 404)

    #print(regex_data["nid"])
    if "invoiceNo" in regex_data:
        del regex_data["invoiceNo"]
    else:
        print("Key 'invoiceNo' does not exist.")
    print(regex_data)
    

    result = user_collection.update_one(
        {"_id": ObjectId(user_id)},      
        {  "$set": {
            "status": "active",
            "regex_data": regex_data
        }
         }, upsert=True
    )

    if result:
        print("filtered and updated")
    # Check if the update was successful
    if result.modified_count == 1:
        return True  # Return True to indicate success
    else:
        return False  # Return False to indicate failure














# def update_collection(user_id, regex_data):
#     invoice_collection = db["bookings"]

#     # print(user_id)
#     existing_user = user_collection.find_one({"_id": ObjectId(user_id)})
#     # print(existing_user['email'])

#     if not existing_user:
#         return jsonify({"error": "User not found"}, 404)

#     # print(regex_data["invoiceNo"])

#     print(regex_data)

#     existing_booking = invoice_collection.find_one(
#         {"invoiceId": regex_data["invoiceNo"]}
#     )
#     if not existing_booking:
#         return jsonify({"error": "book-in not found"}, 404)

#     result = user_collection.update_one(
#         {"_id": ObjectId(user_id)}, {"$set": {"regex_data": regex_data}}, upsert=True
#     )



#     if result:
#         print("filtered and updated")
#     # Check if the update was successful
#     if result.modified_count == 1:
#         return True  # Return True to indicate success
#     else:
#         return False  # Return False to indicate failure








    # Update the collection with the user_id and regex_data
    # result = user_collection.update_one(
    #        {"_id": ObjectId(user_id)},
    # {"$set": {"status": "active"}, "$setOnInsert": {"identity": regex_data}},
    # upsert=True,
    # )