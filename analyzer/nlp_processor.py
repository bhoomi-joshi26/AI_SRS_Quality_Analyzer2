import re
import nltk
import spacy
from nltk.stem import WordNetLemmatizer

# -----------------------------
# Download required NLTK resources
# -----------------------------
resources = {
    "wordnet": "corpora/wordnet",
    "omw-1.4": "corpora/omw-1.4"
}

for resource, path in resources.items():
    try:
        nltk.data.find(path)
    except LookupError:
        nltk.download(resource, quiet=True)

# -----------------------------
# Load spaCy model
# -----------------------------
try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = spacy.blank("en")

STOP_WORDS = nlp.Defaults.stop_words
lemmatizer = WordNetLemmatizer()


# -----------------------------
# Clean text
# -----------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# -----------------------------
# Tokenize text
# -----------------------------
def tokenize_text(text):
    return [token.text for token in nlp(text) if not token.is_space]


# -----------------------------
# Remove stopwords
# -----------------------------
def remove_stopwords(tokens):
    return [word for word in tokens if word not in STOP_WORDS]


# -----------------------------
# Lemmatize words
# -----------------------------
def lemmatize_words(tokens):
    lemmatized = []
    for word in tokens:
        try:
            lemmatized.append(lemmatizer.lemmatize(word))
        except LookupError:
            lemmatized.append(word)
    return lemmatized


# -----------------------------
# Complete preprocessing
# -----------------------------
def preprocess_text(text):
    if not text:
        return ""

    text = clean_text(text)
    tokens = tokenize_text(text)
    tokens = remove_stopwords(tokens)
    tokens = lemmatize_words(tokens)

    return " ".join(tokens)