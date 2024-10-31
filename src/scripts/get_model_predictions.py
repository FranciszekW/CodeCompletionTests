import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

from paths import EXAMPLES_PATH, PREDICTIONS_PATH

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the model and tokenizer
model_name = "tiny_starcoder_py"
model_from = "bigcode/" + model_name
tokenizer = AutoTokenizer.from_pretrained(model_from)
model = AutoModelForCausalLM.from_pretrained(model_from).to(device)

df = pd.read_csv(EXAMPLES_PATH)


def generate_middle_text(prefix, suffix, num_mid_tokens=100):
    # Prepare input text with a placeholder for model to know that it should generate the middle text
    input_text = f"<fim_prefix>{prefix}<fim_suffix>{suffix}<fim_middle>"
    input_ids = tokenizer.encode(input_text, return_tensors='pt').to(device)

    with torch.no_grad():
        output_ids = model.generate(
            input_ids,
            top_p=0.9,
            top_k=50,
            do_sample=True,
            # 2 * mid_length to allow some flexibility in generating the middle text
            max_new_tokens=num_mid_tokens,
            pad_token_id=tokenizer.eos_token_id,
            attention_mask=input_ids.ne(tokenizer.eos_token_id))

    completion = tokenizer.decode(output_ids[0])

    # Extract the middle text from the completion by taking the text after the <fim_middle> token
    # We're not removing the tokens before, because the model could possibly change our
    # prefix or suffix, and then it would be messed up
    generated_text = completion.split("<fim_middle>")[1].strip().replace('<|endoftext|>', "")
    return generated_text


def main():
    # Generate completions for each example
    completions = []
    for index, row in df.iterrows():
        prefix, middle, suffix = row['Prefix'], row['Middle'], row['Suffix']
        num_mid_tokens = len(tokenizer.tokenize(middle))
        generated_middle = generate_middle_text(prefix, suffix,
                                                num_mid_tokens + 15)  # Add some flexibility
        completions.append((middle, generated_middle))

    # Save the completions to a new CSV file
    output_df = pd.DataFrame(completions, columns=['Actual', 'Predicted'])
    output_df.to_csv(PREDICTIONS_PATH, index=False)


if __name__ == '__main__':
    main()
