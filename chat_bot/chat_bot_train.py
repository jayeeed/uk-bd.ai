import re
import random
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import joblib
import nltk
from nltk.corpus import stopwords
from train_question_ans import trian_data
# nltk.download('stopwords')
# nltk.download('punkt')


def word_tokenize_dash_remove_lemmatize(sentence):

    print(f"sentence-------------------- {sentence}")
    stop_words = set(stopwords.words('english'))

    lemmatizer = WordNetLemmatizer()
    lst_words = []

    sentence = sentence.casefold()
    words = word_tokenize(sentence)
    # print(f"tokenize---------{words}")

    lst = []
    # punctuation_pattern = r'[!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]'
    punctuation_pattern = r'[!\"#$%&\'()*+,\-./:;<=>?@\[\\\]^_`{|}~]'

    for word in words:
        # if re.match(punctuation_pattern, word):
        #     continue
        # t = re.split(r'[-]', word)
        t = re.split(punctuation_pattern, word)
        print(f"t-----  {t}")
        for i in t:
            if i.isalpha():
                lst.append(i)
                print(f"lst---------- {lst}")
    lst_words = [w for w in lst if w.lower() not in stop_words]

    for i, element in enumerate(lst_words):
        lst_words[i] = lemmatizer.lemmatize(element, pos='v')

    # print(f"lemmatize----------{lst_words}")
    final = ''.join(i+" " for i in lst_words)
    print(f"----------{final}----------")
    return final


def chat_bot_train(train_data):
    predefined_data = train_data

    # try:
    #     with open("predefined_data.json", "r") as file:
    #         predefined_data = json.load(file)
    # except FileNotFoundError:
    #     predefined_data = []

    # # Append new data to the existing list
    # existing_data.extend(predefined_data)

    # Write the updated data back to the JSON file
    with open("predefined_data.json", "w") as file:
        json.dump(predefined_data, file, indent=4)

    # with open("predefined_data.json", "w") as json_data:
    #     json.dump(predefined_data, json_data)
    if len(predefined_data) > 0:
        for i, record in enumerate(predefined_data):
            predefined_data[i]["question"] = word_tokenize_dash_remove_lemmatize(
                record["question"])
            # predefined_data[i]["answer"] = word_tokenize_dash_remove_lemmatize(
            #     record["answer"])

        # print(predefined_data)  # /////////////////////////////////////////////

        tfidf_vectorizer = TfidfVectorizer()

        # Train the vectorizer on predefined questions
        predefined_questions = [item["question"] for item in predefined_data]
        tfidf_matrix = tfidf_vectorizer.fit_transform(predefined_questions)
        # print(f"tfidf vectorizer--------{tfidf_matrix}")
        joblib.dump(tfidf_matrix, "tfidf_matrix.pkl")
        joblib.dump(tfidf_vectorizer, "tfidf_vectorizer.pkl")
        print("__________training finished__________")

    # Function to retrieve a predefined answer


# chat_bot_train()  # ///////////////////////////////////////
