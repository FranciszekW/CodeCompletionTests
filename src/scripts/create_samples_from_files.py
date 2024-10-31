import os
import random
import csv

from paths import EXAMPLES_PATH


# Split each file into smaller, "independent" code blocks
def extract_code_blocks(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
        # Split the code into blocks based on double newlines
        return code.split('\n\n')


def split_code_block(code_block):
    code_block = code_block.strip()

    if not code_block:  # Handle empty blocks
        return '', '', ''

    total_length = len(code_block)

    # Randomly choose two split points, assuming the code block is at least 20 characters long
    split_point1 = random.randint(total_length // 10,
                                  total_length // 2)  # Don't give too large prefix
    split_point2 = random.randint(split_point1 + 5,  # Ensure the middle is at least 5 characters
                                  total_length - total_length // 10)  # and not too close to the end

    # Create prefix, middle, and suffix based on the split points
    prefix = code_block[:split_point1]
    middle = code_block[
             split_point1:split_point2].strip()  # Middle is what's between the two points
    suffix = code_block[split_point2:]

    return prefix, middle, suffix


def save_examples_to_csv(examples, path):
    # Write examples to a CSV file
    with open(path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Prefix', 'Middle', 'Suffix'])  # Header
        for example in examples:
            writer.writerow(example)


MIN_SAMPLES, MAX_SAMPLES = 2, 5


def main():
    files = ['Eratostenes.java', 'max.asm', 'move_images.py', 'sliding_window.cpp', 'log.c',
             'simple.py']
    all_examples = []

    for file in files:
        file_path = os.path.join('..', '..', 'sample_files', file)
        if os.path.exists(file_path):
            blocks = extract_code_blocks(file_path)
            print(f"Processing code blocks from {file_path}...\n")
            for i, block in enumerate(blocks):
                num_examples = random.randint(MIN_SAMPLES,
                                              MAX_SAMPLES)  # For each block, generate 2-5 examples
                for j in range(num_examples):
                    prefix, middle, suffix = split_code_block(block)
                    all_examples.append((prefix, middle, suffix))

    save_examples_to_csv(all_examples, EXAMPLES_PATH)
    print("Total examples generated:", len(all_examples))
    print(f"Examples saved to {EXAMPLES_PATH}")


if __name__ == '__main__':
    main()
