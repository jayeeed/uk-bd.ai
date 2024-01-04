from pymongo import MongoClient

client = MongoClient('mongodb+srv://ipsita:Ipsita%402023@uk-bd0.u3pngqk.mongodb.net/')

db = client['airbnb']
if db !="None":
    print('connected')
    find_query = "find by Property ID then update the entity with sentiment field"
    review_collection = db['reviews']

    # Assuming your DataFrame is named review_df
    


    