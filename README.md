# Autocorrect — NLP Spelling Correction System

A lightweight **English spelling correction system** built with Python and Natural Language Processing (NLP) techniques.

The system generates candidate corrections using **edit distance operations** and ranks them according to their **frequency-based probability** in a text corpus.

This project was developed as part of my practical study of NLP, with a focus on understanding the algorithms behind autocorrect systems rather than relying on high-level correction libraries.

---

## Overview

The system receives a potentially misspelled English word and attempts to identify the most likely correction.

For example:

```text
Input:
gaod

Candidates:
good
god
...
```

The correction process is based on two main ideas:

1. **Generate possible spelling corrections**
2. **Rank candidates using word probabilities**

The probability of a word is estimated from its frequency in the training corpus:

[\
P(w) = \frac{\text{Count}(w)}{\text{Total number of words}}\
]

Words that occur more frequently in the corpus receive higher probabilities and are therefore ranked higher as correction candidates.

---

## Features

- Text corpus preprocessing
- Sentence tokenization using NLTK
- Word frequency calculation
- Probability estimation for vocabulary words
- One-edit candidate generation
- Two-edit candidate generation
- Optional letter-switch operations
- Vocabulary-based candidate filtering
- Probability-based candidate ranking
- Configurable number of correction suggestions

---

## How It Works

The autocorrect pipeline can be summarized as:

```text
                    Input Word
                        │
                        ▼
                Generate Candidates
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
        One-edit words        Two-edit words
             │                     │
             └──────────┬──────────┘
                        ▼
                  Vocabulary
                    Filtering
                        │
                        ▼
              Calculate / Retrieve
                 Word Probabilities
                        │
                        ▼
                Rank Candidates
                        │
                        ▼
                Top-N Corrections
```

### 1. Corpus Processing

The system starts with a text corpus stored in:

```text
data/text.txt
```

The corpus is divided into sentences using NLTK:

```python
corpus = sent_tokenize(corpus)
```

Each sentence is then passed through the project's preprocessing pipeline.

---

### 2. Building the Probability Dictionary

The `create_probs_dict()` function calculates word frequencies and converts them into probabilities.

```python
def create_probs_dict(corpus):
    freqs = {}
    probs = {}

    for sent in corpus:
        for w in preprocess(sent):
            freqs[w] = freqs.get(w, 0) + 1

    total = sum(freqs.values())

    for k in freqs.keys():
        probs[k] = freqs[k] / total

    return probs
```

The resulting dictionary has the structure:

```python
{
    "the": 0.0521,
    "and": 0.0314,
    "good": 0.0012,
    ...
}
```

The dictionary also acts as the system's vocabulary:

```python
vocab = set(probs.keys())
```

---

## Edit Operations

Candidate words are generated using basic spelling-edit operations.

### Delete

Remove one character:

```text
good → god
```

### Insert

Insert one character:

```text
god → good
```

### Replace

Replace one character:

```text
god → got
```

### Switch

Swap adjacent characters:

```text
gaod → gado
```

These operations are implemented in `edits.py`.

---

## One-Edit Candidates

The `one_edit_set()` function combines all possible one-edit transformations:

```python
def one_edit_set(word, allow_switch=True):
    one_edit_words = (
        edits.delete_letter(word)
        + edits.insert_letter(word)
        + edits.replace_letter(word)
    )

    if allow_switch:
        one_edit_words += edits.switch_letters(word)

    return set(one_edit_words)
```

The result is converted to a `set` to remove duplicate candidates.

---

## Two-Edit Candidates

For words that cannot be corrected using a single edit, the system generates candidates that are up to two edits away.

Conceptually:

```text
word
 ↓
one edit
 ↓
another edit
 ↓
candidate
```

For example:

```text
misspelled
     │
     ├── edit 1
     │
     └── edit 2
          │
          ▼
     valid vocabulary word
```

---

## Candidate Selection

The system prioritizes candidates according to the following strategy:

```text
1. The original word, if it exists in the vocabulary
2. Valid one-edit candidates
3. Valid two-edit candidates
```

The candidates are filtered using:

```python
one_edit_set(word) & vocab
```

This intersection keeps only generated words that actually occur in the corpus.

---

## Ranking Corrections

After generating valid candidates, the system assigns each candidate its corpus probability.

The candidates are then ranked using:

```python
Counter(correct_words).most_common(n)
```

For example:

```python
{
    "good": 0.0041,
    "god": 0.0019,
    "food": 0.0032
}
```

would be ranked according to their probabilities.

The output is:

```python
[
    ("good", 0.0041),
    ("food", 0.0032)
]
```

---

## Project Structure

```text
autocorrect/
│
├── data/
│   └── text.txt
│
├── src/
│   ├── autocorrect.py
│   ├── edits.py
│   └── preprocessing.py
│
├── notebooks/
│   └── test.ipynb
│
├── requirements.txt
├── README.md
└── .gitignore
```

> The exact structure may vary depending on how the project is organized locally.

---

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd autocorrect
```

### 2. Create a virtual environment

Using Conda:

```bash
conda create -n autocorrect python=3.12
conda activate autocorrect
```

Or using Python's built-in virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download NLTK resources

If they are not already installed:

```python
import nltk

nltk.download("punkt")
```

---

## Usage

Place your corpus in:

```text
data/text.txt
```

Then run the main program:

```bash
python src/autocorrect.py
```

The example in the current implementation tests:

```python
word_correct("gaod", probs)
```

The system generates possible corrections and returns the highest-probability candidates.

You can change the input word:

```python
word_correct("recieve", probs)
```

or:

```python
word_correct("teh", probs)
```

The number of returned suggestions can also be changed:

```python
word_correct("gaod", probs, n=5)
```

---

## Example

```text
Input:
gaod

Output:
[
    ('good', 0.00...),
    ('god', 0.00...)
]
```

The exact results depend on the corpus used to build the probability model.

---

## Limitations

The current implementation is intentionally lightweight and has several limitations:

- It uses word frequency as the primary ranking signal.
- It does not consider the surrounding sentence context.
- It does not model grammatical correctness.
- It does not use a neural language model.
- Two-edit generation can produce a large number of candidates.
- Corpus quality strongly affects correction quality.
- Rare words may not be present in the vocabulary.
- Names, abbreviations, and domain-specific terms may be incorrectly corrected.

For example, the correct correction of a word can depend heavily on its surrounding context:

```text
I went to the store.
```

versus:

```text
I stored the data.
```

A frequency-only system cannot fully capture this contextual difference.

---

## Future Improvements

The project can be extended in several directions.

### Context-Aware Correction

Use surrounding words to determine the most likely correction.

Possible approaches include:

- N-gram language models
- Bigram / trigram probabilities
- Neural language models
- Transformer-based models

### Better Candidate Ranking

Instead of ranking only by:

[\
P(w)\
]

the system could combine word probability with edit distance:

[\
Score(w) =\
\lambda P(w) - \mu D(w, x)\
]

where:

- (P(w)) = word probability
- (D(w,x)) = edit distance between the candidate and input
- (\lambda,\mu) = weighting parameters

### TF-IDF Analysis

TF-IDF could be used for corpus analysis and vocabulary exploration, although raw word frequency is generally more directly relevant to this type of autocorrect model.

### Larger and More Diverse Corpora

The model can be trained on larger English corpora containing:

- News
- Wikipedia
- Books
- Conversational text

Combining multiple sources could produce a more representative vocabulary.

### Evaluation

A future version could include a dedicated evaluation dataset and metrics such as:

- Top-1 accuracy
- Top-3 accuracy
- Top-5 accuracy
- Mean Reciprocal Rank (MRR)

---

## Technologies

- **Python**
- **NumPy**
- **Pandas**
- **NLTK**
- **Python Collections**
- **Natural Language Processing**
- **Edit Distance**
- **Probabilistic Language Modeling**

---

## Learning Objectives

This project was built to gain practical understanding of fundamental NLP concepts, including:

- Text preprocessing
- Tokenization
- Vocabulary construction
- Word frequency distributions
- Probability estimation
- String edit operations
- Candidate generation
- Candidate ranking
- Basic language modeling

It also serves as a foundation for progressing toward more advanced NLP systems based on embeddings, neural networks, and Transformer architectures.

**Yousef Magdy Elsayed**

Communication and Computer Engineer\
NLP & Machine Learning Enthusiast

---

## Acknowledgments

This project was developed as part of my practical NLP learning journey and was inspired by classical approaches to spelling correction and probabilistic language modeling.
