from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import re

stop_words = set(stopwords.words("english"))

def preprocess(sentence):
    stemer = PorterStemmer()
    sentence = sentence.lower()
    sentence = re.sub(r"http\S+", "", sentence)
    sentence = re.sub(r"<.*?>", "", sentence)
    sentence = re.sub(r"\s+", " ", sentence).strip()
    sentence = re.sub(r'[^\w\s]', '', sentence)

    sentence = word_tokenize(sentence)
    tokens=[]
    for word in sentence:
        if word not in stop_words:
            word = stemer.stem(word)
            tokens.append(word)
    return tokens