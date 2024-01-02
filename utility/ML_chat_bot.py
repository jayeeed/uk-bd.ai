

import json
import re
from transformers import pipeline
import pickle
from transformers import BertForQuestionAnswering, BertTokenizer
import torch
import os


# RUN JUST ONCE  SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS

model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"

model = BertForQuestionAnswering.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)


# Pickle the model
file_path = os.path.join("data", "qa_model.pkl")
with open(file_path, "wb") as file:
    pickle.dump(model, file)

file_path = os.path.join("data", "tokenizer.pkl")
with open(file_path, "wb") as file:
    pickle.dump(tokenizer, file)
# RUN JUST ONCE  EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE


# Unpickle the model
file_path = os.path.join("data", "qa_model.pkl")
with open(file_path, "rb") as file:
    model = pickle.load(file)
file_path = os.path.join("data", "tokenizer.pkl")
with open(file_path, "rb") as file:
    tokenizer = pickle.load(file)

# Loading the answer corpus SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
ans_corpus = ""
file_path = os.path.join("data", "ans_corpus.txt")

try:
    with open(file_path, "r", encoding="utf-8") as file:
        ans_corpus = file.read()

except FileNotFoundError:
    print(f"The file {file_path} does not exist.")
except Exception as e:
    print(f"An error occurred while reading the file: {e}")


def reload_ans_corpus_file():
    global ans_corpus
    file_path = os.path.join("data", "ans_corpus.txt")

    try:
        with open(file_path, "r", encoding="utf-8-sig") as file:
            ans_corpus = file.read()

    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

# Loading the answer corpus EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE


def get_meaning(question, context):
    input_ids = tokenizer.encode(question, context)
    attention_mask = [1] * len(input_ids)
    output = model(torch.tensor([input_ids]),
                   attention_mask=torch.tensor([attention_mask]))

    # Get the confidence score for the answer
    confidence_score = torch.max(torch.softmax(output.start_logits, dim=1))

    # Get the answer span's start and end indices
    start_index = torch.argmax(output.start_logits)
    end_index = torch.argmax(output.end_logits)

    # Get the answer span from the original text
    answer = tokenizer.decode(
        input_ids[start_index:end_index + 1], skip_special_tokens=True).replace(" @ ", "@").replace(". com", ".com")

    print(f"Answer: {answer}, Confidence Score: {confidence_score.item()}, Start Index: {start_index.item()}, End Index: {end_index.item()}")

    return answer, confidence_score


def find_ans(question):

    context = ans_corpus

    answer, score = get_meaning(question, context)

    if score >= 0.5:
        j = {"answer": answer,
             "question": question,
             "score": score,
             "found": 1
             }
    else:
        j = {"answer": "I don't have the answer.",
             "question": question,
             "score": score,
             "found": 0
             }
    return j


# while True:
#     ans = find_ans(input("input: "))
#     print(f"score--- {ans['score']}  answer----  {ans['answer']}")
