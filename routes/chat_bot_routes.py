
import re
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import joblib
import json
from flask import Flask, request, jsonify, Blueprint
from chat_bot.chat_bot_train import chat_bot_train
# from flask_cors import CORS
from chat_bot.chat_bot import chat_with_chatbot
from chat_bot.mongodb_connection import get_data, overwrite_data, human_ans_post, human_ans_get, predicted_ques_ans_post, predicted_ques_ans_get
from chat_bot.check_if_ques_and_save import is_question, write_sentences_to_json
from chat_bot.hugging_face import find_ans
import asyncio

# to get all the predicted answer with there corresponding question

chatBot_routes = Blueprint("chatBot_routes", __name__)

@chatBot_routes.route("/get_predicted_ques_ans", methods=["GET"])
def get_predicted_ques_ans():
    list_ques_ans = []
    list_ques_ans = predicted_ques_ans_get()
    return jsonify(list_ques_ans)

# to get a question and predict answer from human answer and post to database
@chatBot_routes.route("/predict_ques_ans_and_post", methods=["GET"])
def predict_ques_ans_and_post():
    ques = request.json
    human_ans = human_ans_get()

    if "question" in ques and "human_ans" in human_ans:
        predicted_ans = find_ans(ques["question"], human_ans["human_ans"])

    if (predicted_ans["score"] > 0.6):
        predicted_ques_ans_post()


# to post all the edited question answer to mongodb
@chatBot_routes.route("/post_ques_ans", methods=["POST"])
def post_ques_ans():
    ques_ans = request.json
    if len(ques_ans) > 0:

        overwrite_data(ques_ans)
        # with open("predefined_data.json", "w") as file:
        #     json.dump(ques_ans, file, indent=4)
        # chat_bot_train()
    return jsonify({"response": "Posted"}), 200


# to get all the question answer form mongodb set by the user to view and edit
@chatBot_routes.route("/get_ques_ans", methods=["GET"])
def get_ques_ans():

    question_ans_json = get_data()
    # question_ans_json = predefined_data  # /////////////
    if "train_data" in question_ans_json:  # nedd better check
        return jsonify({"response": question_ans_json["train_data"]}), 200

    # with open("predefined_data.json", "r") as file:
    #     existing_data = json.load(file)
    # return jsonify(existing_data)


# to train the chat bot with newly added question answers
@chatBot_routes.route("/chat_bot_train", methods=["GET"])
def train():
    question_ans_json = get_data()
    # question_ans_json = predefined_data  # /////////////
    if "train_data" in question_ans_json:  # nedd better check
        chat_bot_train(question_ans_json["train_data"])
        print("_____________chatbot train_______________")
        return jsonify({"response": "chat bot trained"}), 200


# to chat with the chat bot
@chatBot_routes.route("/chat_bot", methods=["POST"])
def chat():
    user_query = request.json

    if "text" not in user_query or not isinstance(user_query, dict):
        return jsonify({"error": "Invalid inpu format"}), 400

    else:
        predefined_answer = ""
        if is_question(user_query["text"]):
            predefined_answer = chat_with_chatbot(user_query["text"])
            print("_______________chatbot response_______________")
            print(f"_______{predefined_answer}_________")
            return jsonify({"response": predefined_answer}), 200

        else:
            human_ans_post(user_query["text"])
            return jsonify({"response": " "}), 200

        # if predefined_answer == "I don't have the answer":
        #     find_ans(user_query["text"])

    # if not is_question(user_query["text"]):
    #     write_sentences_to_json(user_query["text"])
    #     human_ans_post(user_query["text"])


# @app.route("/post_ques_ans_single", methods=["POST"])
# def post_ques_ans_single():
#     ques_ans = request.json
#     if len(ques_ans) > 0:

#         try:
#             with open("predefined_data.json", "r") as file:
#                 existing_data = json.load(file)
#         except FileNotFoundError:
#             existing_data = []
#     # Append new data to the existing list
#         existing_data.extend(ques_ans)

#         # Write the updated data back to the JSON file
#         with open("predefined_data.json", "w") as file:
#             json.dump(existing_data, file, indent=4)
#     chat_bot_train()

#     return jsonify({"response": "Posted"}), 200
