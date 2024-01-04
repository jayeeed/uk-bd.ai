import spacy
import json


def is_question(sentence):
    nlp = spacy.load("en_core_web_sm")

    doc = nlp(sentence)

    # Check if the sentence ends with a question mark
    if sentence.strip().endswith("?"):
        print("111111111111111111111")
        return True

    # Check if the root or any token is a question word
    question_words = ["who", "what", "where", "when", "why", "how", "which"]
    for token in doc:
        if token.text.lower() in question_words:
            print("222222222222222222222222222222222")
            return True

    # Check if the sentence contains an auxiliary verb ("is", "can", etc.)
    first_token = doc[0]
    if first_token.pos_ == "AUX":
        print("33333333333333333333333333333333333")
        return True

    return False


def write_sentences_to_json(sentence):
    if not sentence.strip().endswith("."):
        sentence += "."

    with open("corpus.text", 'a') as file:
        file.write(sentence + '\n')
        print("Sentences have been written")


# while True:
#     s = input("input: ")
#     t = is_question(s)
#     print(t)
#     if not t:
#         write_sentences_to_json(s)
#         with open("corpus.text", 'r') as file:
#             content = file.read()
#             print(type(content))
#             print(f"------{content}--------")
