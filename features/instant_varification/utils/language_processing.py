import sys

# install the required packages for both TextRank and LSA algorithms:

import nltk
nltk.download('punkt')
nltk.download('stopwords')

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from heapq import nlargest

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from collections import defaultdict



# !{sys.executable} -m nltk.downloader punkt
# !{sys.executable} -m nltk.downloader stopwords

# Install required packages for Latent Semantic Analysis (LSA) algorithm
# !{sys.executable} -m pip install scikit-learn
# !{sys.executable} -m pip install numpy

# open the file in read mode
file_path = "./output/output_of_scanned_image_to_text.txt"
with open(file_path, 'r') as file:
    # read the contents of the file
    file_contents = file.read()
    # print the contents of the file
    #print(file_contents)

# Function to get the number of sentences in a text file
def get_num_sentences(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
        sentences = nltk.sent_tokenize(text)
        return len(sentences)


def get_summery():
    file_path = "./output/output_of_scanned_image_to_text.txt"
    num_sentences = get_num_sentences(file_path)
    summary = summarize_text(file_path, num_sentences)
    print(summary)
    return(summary)







# Function to get the summary using TextRank algorithm
def summarize_text(file_path, num_sentences):
    
    # Read the text from the file
    with open(file_path, 'r') as file:
        text = file.read()
    
    # Tokenize the text into sentences and words
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    
    # Remove stop words and punctuation marks
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.isalnum() and word not in stop_words]
    
    # Calculate word frequency distribution
    freq_dist = FreqDist(words)
    
    # Build a graph using only top frequent words
    graph = defaultdict(list)
    for i, sentence in enumerate(sentences):
        sentence_words = word_tokenize(sentence.lower())
        sentence_words = [word for word in sentence_words if word.isalnum() and word not in stop_words]
        
        for word in sentence_words:
            if freq_dist[word] >= 2:
                for j in range(i):
                    if word in sentences[j]:
                        graph[j].append(i)
                        graph[i].append(j)
                        break
    
    # Apply PageRank algorithm on the graph
    scores = defaultdict(float)
    for i in range(len(sentences)):
        for j in graph[i]:
            scores[i] += 1 / len(graph[j])
    
    # Get the top sentences based on their scores
    top_sentences = nlargest(num_sentences, scores, key=scores.get)
    top_sentences = [sentences[i] for i in sorted(top_sentences)]
    
    # Combine selected sentences to form a summary
    summary = ' '.join(top_sentences)
    return summary

# # Example usage of the functions
# # file_path = 'example.txt'
# num_sentences = get_num_sentences(file_path)
# summary = summarize_text(file_path, num_sentences)
# print(summary)


















# Function to get the summary using Latent Semantic Analysis (LSA)
# def summarize_text(file_path, num_sentences):
    
#     # Read the text from the file
#     with open(file_path, 'r') as file:
#         text = file.read()

#     # Tokenize the text into sentences
#     sentences = nltk.sent_tokenize(text)
    
#     # Vectorize the sentences using TF-IDF
#     stop_words = set(stopwords.words('english'))
#     stop_words_list = list(stop_words)
#     vectorizer = TfidfVectorizer(stop_words=stop_words_list)
#     sentence_vectors = vectorizer.fit_transform(sentences)
    
#     # Apply Latent Semantic Analysis (LSA) to reduce dimensionality
#     lsa = TruncatedSVD(n_components=1, random_state=0)
#     lsa_vectors = lsa.fit_transform(sentence_vectors)
    
#     # Get the top sentences based on their LSA scores
#     scores = [abs(lsa_vectors[i]) for i in range(len(sentences))]
#     top_sentences = nlargest(num_sentences, range(len(scores)), scores.__getitem__)
#     top_sentences = [sentences[i] for i in sorted(top_sentences)]
    
#     # Combine selected sentences to form a summary
#     summary = ' '.join(top_sentences)
#     return summary

# Example usage of the function
# file_path = 'example.txt'
# num_sentences = get_num_sentences(file_path)
# summary = summarize_text(file_path, num_sentences)
# print(summary)