## Project Overview

This project aims to evaluate the performance of the code completion model
`tiny_starcoder` across various programming languages.

The workflow involved preparing the dataset, running the model to generate code completions, and
then reviewing those outputs both manually and using automated metrics. 

### Introduction

For this project, I chose several files from my personal work,
focusing on different programming languages to test the code completion
model with a variety of examples. I also added a `simple.py` file to see
how the model would handle a short, basic file. All the files were organized
into a `sample_files` directory. Additionally, I created `data` and
`src/scripts` directories to store future CSV files and scripts, respectively.

### Generating Dataset

Initially, I've come up with an idea to split each file into smaller pieces
to create more samples for the model. However, I realized that most files were
already "atomic", so splitting them further could make the task too challenging
for the model. Therefore, I decided to split only two files,`move_images.py`
and `simple.py`, while keeping the other files as single samples after removing
empty lines.

To achieve this, I wrote a script called `create_samples_from_files.py`,
which includes two main functions:

1. `extract_code_blocks`: splits files based on empty lines.
2. `split_code_block`: divides each block into three parts: *prefix*
   (the text before the cursor), *middle* (the missing code to be completed)
   and *suffix* (the text after the cursor).

#### Splitting Method and Challenges

For each code block, I picked two split points almost randomly to create
multiple testing samples, aiming for 2 to 5 samples per block. Why? This
approach would help me see how splitting the same code differently would
affect the model's performance. However, I soon realized that I need to pay
close attention to the split points: each part (prefix, middle, suffix)
had to contain code.

To fix this, I added extra restrictions on the split points in the
`split_code_block` function to make sure no section would be empty and the prefix,
suffix parts wouldn't be too short. This way, the model would receive meaningful
input segments for its completion tasks.

### Running the Model and Getting Predictions

With the dataset ready in `examples.csv`, I created a script called
`get_model_predictions.py` - the name says it all :). I first thought of
using several different models but soon realized that most were too
large for my PC. So, I downloaded the smaller `tiny_starcoder` model,
which indeed was easier and faster to work with, especially after
setting the device to GPU. Also, I found that this model
needs a specific input format for fill-in-the-middle tasks, so I used the
`<fim_prefix>, <fim_middle>, <fim_suffix>` tokens.

One challenge I faced was extracting the generated text from the
model's complete output. After some playing with the tokens, I managed
to get it done. I then tested different hyperparameters to find the best
results. I noticed that sometimes the model would start off well
but wouldn’t finish the prediction. To address this, I added some
flexibility to the `max_new_tokens` parameter by setting it to the
(number of tokens in the actual middle section) + 15.

After fine-tuning, I saved the model predictions alongside the actual
"middle" text in `tiny_starcoder_py_predictions.csv`.

### Manually Reviewing Model Predictions

After saving the predictions, I moved on to reviewing them by hand.
Navigating through CSV files and checking each cell would have been
annoying, so I wrote a script called `rate_completions_manually` to
make this easier. This script shows each sample's `prefix`,
`generated completion`, `actual middle`, and `suffix` in the terminal.
It prompts the user (which was me) to rate each prediction from 1 to 10.
Then it saves the ratings in the first column of a new file,
`tiny_starcoder_metrics.csv`.

I noticed that the model usually did better with popular programming
languages like Python, Java, and C++. Its performance on C was a bit
worse, and it performed really terribly on Assembly (who wouldn't?).
I also found that increasing the prefix had a bigger effect on
improving the model's accuracy than increasing suffix. In addition, the model
generally generated better completions when the desired text was shorter,
but this wasn't always the case (longer Python code was easier than short Assembly).

Manually rating the predictions multiple times (since I tested the
model several times) was definitely the most repetitive part of the
project. However, it was rewarding when the model performed well.
I really got impressed by its accuracy a few times!

### Applying Automated Metrics to Evaluate the Model

Next, I wanted to use some evaluation metrics to check the model's
predictions and see which ones matched my own manual ratings. For this,
I created the `calculate_metrics` script and chose several popular
metrics: `exact_match`, `chrf`, `BLEU`, `ROUGE-L`, and `edit_distance`.
The script goes through each prediction and calculates these metrics.
Then it appends the results to the `tiny_starcoder_metrics.csv` file, next to
the manual ratings' column.

One challenge was that each metric has different input requirements - 
some need strings, while others need lists of strings. I also had to
normalize the metrics to make it easier to compare them. Most metrics
were already normalized, but `edit_distance` wasn't. This metric counts
the number of edits needed to change one code into another. To
normalize it, I divided by the length of the longer string (to fit it
into a 0-1 range) and then subtracted the result from 1. This way,
predictions needing relatively fewer edits would score higher and vice versa.

### Comparing Metrics to Manual Ratings

The final step was to find out which metric is the best (that is, matches my
own manual ratings :)). For this, I created the `choose_best_metric` script.
This script converts each metric column in `tiny_starcoder_metrics.csv`
into a vector and calculates its similarity to the manual ratings column
using cosine similarity. It then prints out similarities for each metric
and the winner (metric with the highest similarity score).

Interestingly, the results changed with different datasets and predictions.
In general, `chrF` and `ROUGE-L` were the best, while `BLEU` and `edit_distance`
did a little worse. `Exact match` was consistently losing. It wasn't a surprise,
as the model rarely generated the exact same middle code segment. In fact, it
happened only about five times throughout all my tests.

Overall, this comparison gave useful insights into which metrics best reflect
human judgment when evaluating code completions, although it also showed some
variability depending on the specific dataset and model predictions.

### Conclusion

I really enjoyed working on this project. It gave me valuable insights into 
working with code completion models and the challenges of evaluating their
effectiveness. Throughout the process, I felt a range of emotions - from laughter
at the silly responses generated by the model to amazement at its unexpected
accuracy.

I am very grateful for the chance to work on such an interesting and
educational project.