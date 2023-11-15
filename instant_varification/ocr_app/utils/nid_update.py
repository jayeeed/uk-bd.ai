        # "nid": regex_data['nid'],
        # "dob": regex_data['dob'] 
from flask import jsonify

def update_collection(user_id, regex_data):
    import pymongo
    client = pymongo.MongoClient("mongodb+srv://ipsita:Ipsita%402023@uk-bd0.u3pngqk.mongodb.net/")
    db = client["airbnb"]
    user_collection = db["users"]
    invoice_collection = db["bookings"]

    #print(user_id)
    existing_user = user_collection.find_one({'_id': user_id})
    print(existing_user['email'])
    if not existing_user:
        return jsonify({'error': 'User not found'}, 404)
    
    print(regex_data["invoiceNo"])
    
    existing_booking =  invoice_collection.find_one({'invoiceId': regex_data["invoiceNo"]})
    if not existing_booking:
        return jsonify({'error': 'book-in not found'}, 404)



    # Update the collection with the user_id and regex_data
    result = user_collection.update_one(
        {'_id': user_id},
        {'$set': {'status': "active",'identity': regex_data}
         # '$setOnInsert': {'identity': regex_data}
        },
        upsert=True
    )

    if result:
        print("filtered")
    # Check if the update was successful
    if result.modified_count == 1:
        return True  # Return True to indicate success
    else:
        return False  # Return False to indicate failure