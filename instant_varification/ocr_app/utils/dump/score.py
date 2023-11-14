from rouge_score import rouge_scorer

def calculate_rouge_scores(hypotheses, references):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2'], use_stemmer=True)
    scores = scorer.score(hypotheses, references)
    return scores

# Example usage:
hypotheses = "these are some words"
references = "these are some other words here are some reference words"

Read in file
with open('example_file.txt', 'r') as f:
    file_contents = f.readlines()

# Preprocess file contents to remove newline characters
file_contents = [line.strip() for line in file_contents]

# Define reference summaries as a list of strings
reference_summaries = ["Here is a summary of the article.", 
                       "This article discusses the impact of social media on mental health."]

# Calculate ROUGE scores
scores = calculate_rouge_scores(file_contents, reference_summaries)

# Print scores
print('ROUGE scores:', scores)



scores = calculate_rouge_scores(hypotheses, references)
print('ROUGE scores:', scores)