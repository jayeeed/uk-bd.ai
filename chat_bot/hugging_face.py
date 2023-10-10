# import re
# from transformers import pipeline
# from train_question_ans import ques_ans, para

# # Step 1: Reading and Tokenization


# def tokenize_text(text):
#     tokens = text.split()
#     return tokens

# # Step 2: Text Preprocessing


# def preprocess_tokens(tokens):
#     preprocessed_tokens = [
#         re.sub(r'[^\w\s]', '', token.lower()) for token in tokens]
#     return preprocessed_tokens

# # Step 3: Understanding Meaning (using a pre-trained language model)


# def get_meaning(tokens):
#     nlp = pipeline("question-answering")
#     context = " ".join(tokens)
#     question = "tell me about liberation warof bangladesh"
#     result = nlp(question=question, context=context)
#     return result["answer"]


# # Example text
# user_input = ques_ans

# # Step 1: Tokenization
# tokenized_text = tokenize_text(user_input)

# # Step 2: Preprocessing
# preprocessed_tokens = preprocess_tokens(tokenized_text)

# # Step 3: Understanding Meaning
# answer = get_meaning(preprocessed_tokens)

# print("Question:", user_input)
# print("Answer:", answer)

import json
import re
from transformers import pipeline
from train_question_ans import ques_ans, para

# Step 1: Reading and Tokenization


def tokenize_text(text):
    tokens = text.split()
    return tokens

# Step 2: Text Preprocessing


def preprocess_tokens(tokens):
    preprocessed_tokens = [
        re.sub(r'[^\w\s]', '', token.lower()) for token in tokens]
    return preprocessed_tokens

# Step 3: Understanding Meaning (using a pre-trained language model)


def get_meaning(context, question):
    nlp = pipeline("question-answering")
    result = nlp(question=question, context=context)

    answer = result["answer"]
    score = result["score"]
    return answer, score


def find_ans(question, human_ans):
    # with open("corpus.text", 'r') as file:
    #     user_input = file.read()
    # # Example text and context
    # context = " ".join(preprocess_tokens(tokenize_text(user_input)))
    context = human_ans

    answer, score = get_meaning(context, question)

    # if score >= 0.6:
    j = {"answer": answer,
         "question": question,
         "score": score
         }
    return j

    #     try:
    #         with open("predicted_ques_ans.json", "r") as file:
    #             existing_data = json.load(file)
    #     except FileNotFoundError:
    #         existing_data = []

    # # Append new data to the existing list
    #     existing_data.extend(j)

    #     # Write the updated data back to the JSON file
    #     with open("predicted_ques_ans.json", "w") as file:
    #         json.dump(existing_data, file, indent=4)

    #     print("Question:", question)
    #     print("Answer:", answer)

    # else:
    #     print("------no ans------")
    #     print("Answer:", answer)


# find_ans("what is the national fruit of bangladesh?")
