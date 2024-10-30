import pandas as pd

# Load the datasets
examples_df = pd.read_csv('../../examples_dataset.csv')
completions_df = pd.read_csv('../../tiny_starcoder_py.csv')

# Define the model name (e.g., "tiny_starcoder")
model_name = "tiny_starcoder"

# Add model name as a column if not already in ratings_df
if 'Manual rating' not in completions_df.columns:
    completions_df['Manual rating'] = None

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
    completions_df.at[index, 'Manual rating'] = rating

    # Save ratings after each input to prevent data loss
    completions_df.to_csv('ratings.csv', index=False)

print("\nAll ratings have been saved to ratings.csv.")
