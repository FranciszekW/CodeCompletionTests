import pandas as pd

from paths import EXAMPLES_PATH, PREDICTIONS_PATH, METRICS_PATH

# Load the datasets
examples_df = pd.read_csv(EXAMPLES_PATH)
completions_df = pd.read_csv(PREDICTIONS_PATH)

metrics_df = pd.DataFrame(index=range(len(completions_df)))
# Clear the csv file if it already exists
metrics_df.to_csv(METRICS_PATH, index=False)

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
    metrics_df.to_csv(METRICS_PATH, index=False)

print(f"\nManual metrics have been saved to {METRICS_PATH}.")