import pandas as pd
from transformers.models.pop2piano.convert_pop2piano_weights_to_hf import model

df = pd.read_csv('../../examples_dataset.csv')

from transformers import AutoTokenizer, AutoModel

# Load the model and tokenizer
model_name = "bigcode/tiny_starcoder"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

import torch
def generate_middle_text(prefix, suffix, mid_length=50):
    input_text = prefix + tokenizer.eos_token + suffix
    input_ids = tokenizer.encode(input_text, return_tensors='pt')

    with torch.no_grad():
        # 2 * mid_length to allow some flexibility in the generated middle text
        output_ids = model.generate(input_ids, max_length=len(input_ids[0]) + 2 * mid_length, pad_token_id=tokenizer.eos_token_id)

    completion = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    generated_text = completion[len(prefix):completion.rfind(suffix)].strip()

    return generated_text

# Generate completions for each example
completions = []
for index, row in df.iterrows():
    prefix, middle, suffix = row['Prefix'], row['Middle'], row['Suffix']
    generated_middle = generate_middle_text(prefix, suffix, len(middle))
    completions.append((prefix, generated_middle, suffix))

# Save the completions to a new CSV file
output_df = pd.DataFrame(completions, columns=['Prefix', 'Middle', 'Suffix'])
output_df.to_csv('../../completions_dataset.csv', index=False)