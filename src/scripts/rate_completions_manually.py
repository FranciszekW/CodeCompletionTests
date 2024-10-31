import pandas as pd

# Load the datasets
examples_df = pd.read_csv('../../data/examples_dataset.csv')
completions_df = pd.read_csv('../../data/tiny_starcoder_py.csv')

# Define the model name (e.g., "tiny_starcoder")
model_name = "tiny_starcoder"

# Create metrics dataframe if it doesn't exist
try:
    metrics_df = pd.read_csv('../../data/tiny_starcoder_metrics.csv')
except FileNotFoundError:
    metrics_df = pd.DataFrame(index=range(len(completions_df)))

# Add model name as a column if not already in metrics_df
if model_name not in metrics_df.columns:
    metrics_df['Manual'] = None

# Loop over each example and prompt for rating
for index, (example_row, completion_row) in enumerate(
        zip(examples_df.itertuples(), completions_df.itertuples())):
    # Display information for comparison
    print("\n---------------------------")
    print(f"Example {index + 1}")
    print("---------------------------")
    print("Prefix:\n", example_row.Prefix, "\n")
    print("Generated Completion:\n", completion_row.Predicted, "\n")
    print("Actual Middle (Target Completion):\n", example_row.Middle, "\n")
    print("Suffix:\n", example_row.Suffix, "\n")

    # Prompt for a rating
    while True:
        try:
            rating = int(input("Enter your rating (1-10) for this completion: "))
            if 1 <= rating <= 10:
                break
            else:
                print("Please enter a number between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    # Save the rating to the DataFrame
    metrics_df.at[index, 'Manual'] = rating

    # Save metrics after each input to prevent data loss
    metrics_df.to_csv('../../data/tiny_starcoder_metrics.csv', index=False)

print("\nAll metrics have been saved to tiny_starcoder_metrics.csv.")