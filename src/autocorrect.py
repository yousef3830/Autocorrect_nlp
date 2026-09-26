import edits
from preprocessing import preprocess
from nltk.tokenize import sent_tokenize
from collections import Counter

def create_probs_dict(corpus):
    freqs = {}
    probs = {}
    for sent in corpus:
        for w in preprocess(sent):
            freqs[w] = freqs.get(w,0) + 1

    total = sum(freqs.values())
    for k in freqs.keys():
        probs[k] = freqs.get(k,0) / total
    return probs


def one_edit_set(word,allow_switch = True):
    one_edit_words = edits.delete_letter(word) + edits.insert_letter(word) + edits.replace_letter(word)
    if allow_switch:
        one_edit_words += edits.switch_letters(word)
    return set(one_edit_words)


def two_edits_set(word,allow_switch = True):
    one_edit_words = one_edit_set(word,allow_switch)
    two_edit_words = set()
    for w in one_edit_words:
        two_edit_words.update(one_edit_set(w, allow_switch))    
    return two_edit_words

def word_correct(word,probs,n = 2):
    vocab = set(probs.keys())
    correct_words = {}
    suggestions = ({word} & vocab or
                   one_edit_set(word) & vocab or
                   two_edits_set(word) & vocab)
    for w in suggestions:
        correct_words[w] = probs.get(w,0)
    top_n = Counter(correct_words).most_common(n)
    return top_n


if __name__ == "__main__":
    path = "data/"

    with open(path +"text.txt") as f:
        corpus = f.read()

    corpus = sent_tokenize(corpus)
    probs = create_probs_dict(corpus)
    print(word_correct("gaod",probs))