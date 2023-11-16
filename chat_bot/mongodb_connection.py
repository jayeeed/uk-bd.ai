# from flask import jsonify, Flask

from db.db_config import chatbot_predicted_ques_ans_collection ,chatbot_question_ans_collection,chatbot_human_ans_collection 

# from flask_cors import CORS
# from flask_pymongo import PyMongo

# app = Flask(__name__)
# CORS(app)
# app.config["MONGO_URI"] = "mongodb+srv://ipsita:Ipsita%402023@uk-bd0.u3pngqk.mongodb.net/airbnb"
# try:
#     mongo = PyMongo(app)
#     print("____________________connection successfull____________________________")

# except Exception as e:
#     print(f"error________________{e}")

# gets all the question answer from the database


def get_data():
    question_ans = []
    collection = chatbot_question_ans_collection  
    data = list(collection.find({}))

    if len(data) > 0:
        print(data)
        for item in data:
            question_ans.append(
                {"question": item["question"], "answer": item["answer"]})

        print(question_ans)
        return {"train_data": question_ans}
    else:
        return {"train_data": " "}

# this fuction posts all the ques ans after user sets or alters them


def overwrite_data(new_data):
    # Specify the collection name (replace 'chatbot_question_ans' with your actual collection name)

    try:
        collection = chatbot_question_ans_collection
    except Exception as e:
        print(f"error________________{e}")

    # Delete all existing documents in the collection

    try:
        collection.delete_many({})
        for json_obj in new_data:
            collection.insert_one(json_obj)

    # Insert the new data into the collection
    except Exception as e:
        print(f"error________________{e}")

    return {'message': 'Collection overwritten with new data'}


# posts all the human answers to the database for finding ans dynamically
def human_ans_post(human_ans):

    json_obj = {"human_ans": human_ans}

    try:
        collection = chatbot_human_ans_collection

        collection.insert_one(json_obj)
        return {'message': 'human ans uploaded'}
    except Exception as e:
        print(f"error________________{e}")


def human_ans_get():
    human_ans = []
    str = ""
    collection = chatbot_human_ans_collection 

    data = list(collection.find({}))
    print(data)
    for item in data:
        str = str+item["human_ans"]

    print(human_ans)
    return {"human_ans": str}


def predicted_ques_ans_post(predicted_ans):

    try:
        collection = chatbot_predicted_ques_ans_collection
        collection.insert_one(predicted_ans)
        return {'message': 'predicted answer uploaded'}
    except Exception as e:
        print(f"error________________{e}")


def predicted_ques_ans_get(predicted_ans):

    question_ans = []

    try:
        collection = chatbot_predicted_ques_ans_collection
        data = list(collection.find({}))
    except Exception as e:
        print(f"error________________{e}")

    if len(data) > 0:
        print(data)
        for item in data:
            question_ans.append(
                {"question": item["question"], "answer": item["answer"]})

        # print(question_ans)
        return {"predicted_ques_ans": question_ans}
    else:
        return {"predicted_ques_ans": " "}


# get_data()

# if __name__ == "__main__":
#     app.run(debug=True)
