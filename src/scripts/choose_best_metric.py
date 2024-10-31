import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
file_path = "../../data/tiny_starcoder_metrics.csv"
data = pd.read_csv(file_path)

# Extract  manual ratings as a column vector (that's what the cosine_similarity function expects)
manual_ratings = data['Manual'].values.reshape(1, -1)

# Calculate cosine similarities
cosine_similarities = {}
for metric in data.columns:
    if metric not in ['Manual']:
        metric_column = data[metric].values.reshape(1, -1)  # Convert to column vector
        similarity = cosine_similarity(metric_column, manual_ratings)[0][0]
        cosine_similarities[metric] = similarity

# Print the similarities
print("Cosine Similarities with Manual Ratings:")
for metric, similarity in cosine_similarities.items():
    print(f"{metric}: {similarity:.4f}")

print("\nAnd the winner is:", max(cosine_similarities, key=cosine_similarities.get))
