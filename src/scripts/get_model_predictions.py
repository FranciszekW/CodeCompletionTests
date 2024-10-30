import pandas as pd

df = pd.read_csv('../../examples_dataset.csv')

from transformers import AutoTokenizer, AutoModelForCausalLM

# Load the model and tokenizer
model_name = "bigcode/tiny_starcoder_py"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

import torch


def generate_middle_text(prefix, suffix, mid_length=100):
    # Prepare input text with a placeholder for model to know where it should generate the middle text
    input_text = f"<fim_prefix>{prefix}<fim_suffix>{suffix}<fim_middle>"
    input_ids = tokenizer.encode(input_text, return_tensors='pt')

    with torch.no_grad():
        output_ids = model.generate(
            input_ids,
            # 2 * mid_length to allow some flexibility in generating the middle text
            max_length=len(input_ids[0]) + 2 * mid_length,
            pad_token_id=tokenizer.eos_token_id,
            attention_mask=input_ids.ne(tokenizer.eos_token_id))

    completion = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    # Extract the middle text from the completion
    # generated_text = completion[len(prefix):completion.rfind(suffix)].strip()

    print(completion)
    return completion


# Generate completions for each example
completions = []
for index, row in df.iterrows():
    prefix, middle, suffix = row['Prefix'], row['Middle'], row['Suffix']
    generated_middle = generate_middle_text(prefix, suffix, len(middle))
    completions.append((prefix, generated_middle, suffix))

# Save the completions to a new CSV file
output_df = pd.DataFrame(completions, columns=['Prefix', 'Middle', 'Suffix'])
output_df.to_csv('../../completions_dataset.csv', index=False)
