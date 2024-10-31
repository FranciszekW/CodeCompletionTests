import pandas as pd
from nltk.translate.chrf_score import sentence_chrf
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge import Rouge
import editdistance

# Load the completions dataset
completions_df = pd.read_csv('../../data/tiny_starcoder_py.csv')
results_df = pd.read_csv('../../data/tiny_starcoder_metrics.csv')

# Initialize metrics
rouge = Rouge()

# Prepare lists to hold results
exact_match_scores = []
chrf_scores = []
bleu_scores = []
rouge_l_scores = []
edit_distance_scores = []

# Loop over each completion
for index, row in completions_df.iterrows():
    actual = row['Actual']
    predicted = row['Predicted']

    # Calculate Exact Match
    exact_match = int(actual == predicted)
    exact_match_scores.append(exact_match)

    # Calculate ChrF
    chrf_score = sentence_chrf([actual], [predicted])
    chrf_scores.append(chrf_score)

    # Calculate CodeBLEU
    bleu_score = sentence_bleu([actual.split()], predicted.split(), smoothing_function=SmoothingFunction().method1)
    bleu_scores.append(bleu_score)

    # Calculate ROUGE-L
    rouge_scores = rouge.get_scores([predicted], [actual])
    rouge_l = rouge_scores[0]['rouge-l']['f']
    rouge_l_scores.append(rouge_l)

    # Calculate Edit Distance
    # Normalize the edit distance by dividing by the maximum length of the two strings
    edit_distance = editdistance.eval(actual, predicted)
    max_len = max(len(actual), len(predicted))
    normalized_edit_distance = edit_distance / max_len if max_len > 0 else 0
    # We want to give higher scores when less changes are needed, so we invert the normalized edit distance
    inverted_edit_distance = 1 - normalized_edit_distance
    edit_distance_scores.append(inverted_edit_distance)

# Append results to DataFrame
results_df['Exact Match'] = exact_match_scores
results_df['chrF'] = chrf_scores
results_df['BLEU'] = bleu_scores
results_df['ROUGE-L'] = rouge_l_scores
results_df['Edit Distance'] = edit_distance_scores

# Append the results to metrics csv
results_df.to_csv('../../data/tiny_starcoder_metrics.csv', index=False)

print("Metrics have been calculated and saved to tiny_starcoder_metrics.csv.")