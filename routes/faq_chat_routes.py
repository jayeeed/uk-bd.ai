# /home/vaib/Desktop/projectB/uk-bd.ai/faq_chat

from flask import request, jsonify, Blueprint
from flask_cors import CORS, cross_origin
from features.faq_chat.ml_models.faq_chat_model import get_data, overwrite_data, overwrite_data
from features.faq_chat.utility.ML_chat_bot import find_ans, reload_ans_corpus_file
from features.faq_chat.utility.check_ans import is_ans
from features.faq_chat.utility.is_question import is_ques, add_question_mark

# to get all the question answer form mongodb set by the user to view and edit
faq_chat_route = Blueprint('faq_chat_route', __name__)

CORS(faq_chat_route)
# CORS(price_predict_routes, resources={
#     r"/api/faq_chat_route": {"origins": "http://localhost:3009"})

@faq_chat_route.route("/ans_corpus_get", methods=["GET"])  # type: ignore
def ans_corpus_get():
    ans_corpus = get_data()
    if "text" in ans_corpus:  # nedd better check  # type: ignore
        print("--------------------------------reload ans corpus-----------------------------------")
        reload_ans_corpus_file()
        return jsonify({"response": ans_corpus["text"]}), 200


# to train the chat bot with newly added question answers
@faq_chat_route.route("/ans_corpus_post", methods=["POST"])
def ans_corpus_post():
    ans_corpus = request.json
    if "text" not in ans_corpus:  # or not isinstance(ans_corpus, dict):   # type: ignore
        return jsonify({"error": "Invalid inpu format"}), 400
    else:
        overwrite_data(ans_corpus["text"])
        return jsonify({"response": "Posted"}), 200


question = {
    "exist": 0,
    "ques": ""
}


@faq_chat_route.route("/check_ans", methods=["POST"])  # type: ignore
def check_ans():
    vendor_ans = request.json

    if "text" not in vendor_ans or not isinstance(vendor_ans, dict): 
        return jsonify({"error": "Invalid inpu format"}), 400

    if is_ques(vendor_ans["text"]):
        question["exist"] = 1
        question["ques"] = vendor_ans["text"]

    else:
        if question["exist"]:
            answer = is_ans(question["ques"], vendor_ans["text"])
            if answer["found"]:
                file_path = "ans_corpus.txt"

                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        ans_corpus = file.read()
                except FileNotFoundError:
                    print(f"The file {file_path} does not exist.")
                except Exception as e:
                    print(f"An error occurred while reading the file: {e}")

                if not vendor_ans["text"].strip().endswith("."):
                    vendor_ans["text"] += "."
                ans_corpus = ans_corpus + vendor_ans["text"]
                overwrite_data(ans_corpus)

                return jsonify({"response": answer['answer']}), 200
            else:
                return jsonify({"response": "No answer found."}), 200

        else:
            return jsonify({"response": "No question available"}), 200


# to chat with the chat bot
@faq_chat_route.route("/api/chat_bot", methods=["POST"])
def chat():
    user_query = request.json

    # type: ignore
    if "text" not in user_query or not isinstance(user_query, dict):
        return jsonify({"error": "Invalid inpu format"}), 400

    else:
        answer = ""
        user_query["text"] = add_question_mark(user_query["text"])
        answer = find_ans(user_query["text"])
        if not answer["found"]:
            question["exist"] = 1
            question["ques"] = answer["question"]
            print(f"----------------{ question['ques']}---------------")

        print("_______________chatbot response_______________")
        print(f"_______{answer['answer']}_________")
        return jsonify({"response": answer['answer']}), 200


