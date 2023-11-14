def reservationCheck():
	    import pymongo

    client = pymongo.MongoClient("mongodb+srv://df3@uk-bd0.u3pngqk.mongodb.net/")
    db = client["airbnb"]
    booking_collection = db["bookings"]
    # user_collection = db 

    # result = booking_collection.find("")

    

    query = {"userId": <user_id>, "propertyId": <property_id>}

    data = collection.aggregate([
        {
            "$match": query
        },
        {
            "$lookup": {
                "from": "users",
                "localField": "userId",
                "foreignField": "_id",
                "as": "user"
            }
        },
        {
            "$lookup": {
                "from": "payments",
                "localField": "paymentId",
                "foreignField": "_id",
                "as": "payment"
            }
        },
        {
            "$lookup": {
                "from": "properties",
                "localField": "propertyId",
                "foreignField": "_id",
                "as": "property"
            }
        },
        {
            "$project": {
                "_id": 0,
                # "bookingid": { "$toString": "$_id" },
                "paymentid": { "$toString": "$paymentId" },
                "username": { "$arrayElemAt": ["$user.username", 0] },
                "email": { "$arrayElemAt": ["$user.email", 0] },
                "booking_startdate": { "$dateToString": { "format": "%Y-%m-%d", "date": "$startDate" } },
                "booking_enddate": { "$dateToString": { "format": "%Y-%m-%d", "date": "$endDate" } },
                "payment_created_At": { "$arrayElemAt": ["$payment.created_At", 0] },
                "property_name": { "$arrayElemAt": ["$property.title", 0] },
                "property_address": { "$arrayElemAt": ["$property.address", 0] }
            }
        },
        {
        "$limit": 15
    	}
    ])

    for d in data:
        print(d)