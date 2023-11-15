def info_matching(info):
    #print(type(info))

    import pymongo
    client = pymongo.MongoClient("mongodb+srv://ipsita:Ipsita%402023@uk-bd0.u3pngqk.mongodb.net/")
    db = client["airbnb"]

    if db != None :
        print("db connected")

        if info["nid"]:
            query = {"nid": info["nid"]}
            print("nid :",info["nid"])
        else:
            query = {"invoiceId": info["invoiceNo"]}
            print("invoiceNo :",info["invoiceNo"])


        

        # Get the users collection
        users_collection = db["users"]
        invoice_collection = db["bookings"]

        # Find the user with the given nid key
        try:
            user = users_collection.find_one(query)
            invoice_checked = invoice_collection.find_one(query)
            # print(user.email)
            # print(user["email"])
        except Exception as e:
            print(e)

        # for user in users:
        #     print(user)

        # user = users_collection.find_one(query)
        if user is not None:
            print("National-ID found in users collection ==> ", user["email"])
            return "Id Found"
        elif invoice_checked is not None:
            print("Invoice-ID found in booking collection ==> ", invoice_checked["invoiceId"])
            return "Invoice Found"
        else:
            print("National ID or Invoice not found in Database")
    return 0

    # if db != None :
    #     print("db connected")

    # print("nid :",info["nid"])
    # query = {"nid": info["nid"]}

    # # Get the payments collection
    # payments_collection = db["payments"]

    # # Define the pipeline to lookup the user details from the users table
    # lookup_pipeline = [
    #     {
    #         "$match": query
    #     },
    #     {
    #         "$lookup": {
    #             "from": "users",
    #             "localField": "userId",
    #             "foreignField": "_id",
    #             "as": "user"
    #         }
    #     },
    #     {"$unwind": "$user"},
    #     {"$project": {"user.username": 1, "user.email": 1 , "user.nid":1}}
    # ]

    # # Find the payments and lookup the user details
    # for payment in payments_collection.aggregate(lookup_pipeline):
    #     print(" National id card found in payment table ==>  ", payment)
    #     if payment:
    #         return r'okay'

    # return 0
    # return r'okay'






# import pymongo
# client = pymongo.MongoClient("mongodb+srv://ipsita:Ipsita%402023@uk-bd0.u3pngqk.mongodb.net/")
# db = client["airbnb"]
# collection = db["invoices"]
# query = {"nid": 150369974}
# result = collection.find(query)

# data = []
# for doc in result:
#     data.append(doc)

#print(data)







    
    # collection = db["users"]

    # query = {"nid": info["nid"]}

    # for data in collection.find().limit(15):
    #     print()

    # query = {"nid": 1504946484}
    # try:
    #     result = collection.find(query)
    # except:
    #     print("User not found")


    # data = []
    # for doc in result:
    #     data.append(doc)

    # print(data)
