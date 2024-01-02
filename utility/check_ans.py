

import json
import re
from transformers import pipeline
import pickle
import spacy
from utility.ML_chat_bot import get_meaning
nlp = spacy.load("en_core_web_sm")


def similarity_of_sentences_subj(sentence_1, sentence_2):

    subj_1 = subject_of_sentence(sentence_1)
    subj_2 = subject_of_sentence(sentence_2)

    if len(subj_1) != len(subj_2):
        return False

    for i in range(len(subj_1)):
        if subj_1[i] != subj_2[i]:
            return False

    return True


def subject_of_sentence(sentence):
    # Load the English language model
    print(f"sentence------------------------------------ {sentence}")
    # Process the sentence
    # sentence = "Riki and Roy are good friends"
    doc = nlp(sentence)

    # Initialize a list to store multiple subjects
    subjects = []

    # Iterate through the tokens in the sentence
    for token in doc:
        # Check if the token is a subject (nsubj) or a conjunction (conj)
        if "nsubj" in token.dep_ or "conj" in token.dep_:
            # Append the text of the token to the list of subjects
            subjects.append(token.text)
            print(f"Subjects in the sentence: {token.text}")

    # Print the list of subjects
    # if subjects:
    #     print(f"Subjects in the sentence: {', '.join(subjects)}")
    return subjects


# def get_ans(question, context):
#     # model_checkpoint = "huggingface-course/bert-finetuned-squad"
#     # nlp = pipeline("question-answering", model=model_checkpoint)
#     with open("qa_model.pkl", "rb") as file:
#         nlp = pickle.load(file)

#     result = nlp(question=question, context=context)
#     answer = result["answer"]
#     score = result["score"]
#     print(result)
#     return answer, score


def is_ans(question, context):

    # context = "yes, bangladesh is an independent country. Capital of indonesia is dhaka. it's size is 570 square kilometre."

    match = similarity_of_sentences_subj(question, context)

    if match:
        answer, score = get_meaning(question, context)

        if score >= 0.7:
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
    else:
        j = {"answer": "I don't have the answer.",
             "question": question,
             "score": 0,
             "found": 0
             }
        return j

# while True:
#     ans = is_ans(input("input: "))
#     print(f"score--- {ans['score']}  answer----  {ans['answer']}")
