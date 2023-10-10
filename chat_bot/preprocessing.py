import spacy
import re
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import joblib

# Load the English language model
nlp = spacy.load("en_core_web_sm")


def complex_preprocessing(text):
    # Step 1: Tokenization, Lowercasing
    doc = nlp(text.lower())

    # Step 2: Remove Punctuation
    tokens_without_punct = [token for token in doc if not token.is_punct]

    # Step 3: Remove Stop Words
    tokens_without_stop = [
        token for token in tokens_without_punct if not token.is_stop]

    # Step 4: Lemmatization
    lemmatized_tokens = [token.lemma_ for token in tokens_without_stop]

    # Step 5: Part-of-Speech Tagging
    pos_tags = [token.pos_ for token in tokens_without_stop]

    # Step 6: Named Entity Recognition (NER)
    named_entities = [(ent.text, ent.label_) for ent in doc.ents]

    # Step 7: Dependency Parsing
    dependencies = [(token.text, token.dep_) for token in tokens_without_stop]

    return {
        "tokens": lemmatized_tokens,
        "pos_tags": pos_tags,
        "named_entities": named_entities,
        "dependencies": dependencies
    }


# Example sentence
sentence = "Apple Inc. is planning to build a new headquarters in Cupertino."

# Apply complex preprocessing
preprocessed_output = complex_preprocessing(sentence)

# Print the preprocessed output
print(preprocessed_output)


def word_tokenize_dash_remove_lemmatize(sentence):
    lemmatizer = WordNetLemmatizer()
    lst_words = []
    sentence = sentence.casefold()
    words = word_tokenize(sentence)
    # print(f"tokenize---------{words}")
    lst = []
    for word in words:
        t = re.split(r'[-]', word)
        for i in t:
            lst.append(i)
    # print(f"split----------{lst}")
    for i in lst:
        lst_words.append(lemmatizer.lemmatize(i))

    # print(f"lemmatize----------{lst_words}")
    return ''.join(i+" " for i in lst_words)


# while True:
#     t = input("input:")
#     print(word_tokenize_dash_remove_lemmatize(t))
w = "was"
print(WordNetLemmatizer().lemmatize(w, pos="v"))
