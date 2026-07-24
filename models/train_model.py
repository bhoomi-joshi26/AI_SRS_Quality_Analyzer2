import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
# =====================================================
# PROJECT PATHS
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(
    BASE_DIR,
    "..",
    "dataset",
    "srs_dataset.csv"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "model.pkl"
)

VECTORIZER_PATH = os.path.join(
    MODEL_DIR,
    "vectorizer.pkl"
)

os.makedirs(MODEL_DIR, exist_ok=True)

# =====================================================
# LOAD DATASET
# =====================================================

df = pd.read_csv(DATASET_PATH)

print("Dataset Loaded Successfully")

print("Total Samples :", len(df))
# =====================================================
# CLEAN DATASET
# =====================================================

df = df.dropna()

df = df.drop_duplicates(
    subset="requirement"
)

df["requirement"] = (
    df["requirement"]
    .astype(str)
    .str.strip()
)

print("Samples After Cleaning :", len(df))

# =====================================================
# INPUT & OUTPUT
# =====================================================

X = df["requirement"]

y = df["label"]

# =====================================================
# TF-IDF
# =====================================================

vectorizer = TfidfVectorizer(

    lowercase=True,

    stop_words="english",

    ngram_range=(1,2),

    max_features=5000

)

X_vector = vectorizer.fit_transform(X)
# =====================================================
# TRAIN TEST SPLIT
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(

    X_vector,

    y,

    test_size=0.20,

    random_state=42,

    stratify=y

)

# =====================================================
# RANDOM FOREST MODEL
# =====================================================

model = RandomForestClassifier(

    n_estimators=300,

    random_state=42

)

model.fit(

    X_train,

    y_train

)
# =====================================================
# MODEL EVALUATION
# =====================================================

prediction = model.predict(X_test)

accuracy = accuracy_score(

    y_test,

    prediction

)

print("\nAccuracy :")

print(round(accuracy * 100,2), "%")

print("\nClassification Report")

print(

    classification_report(

        y_test,

        prediction

    )

)

print("\nConfusion Matrix")

print(

    confusion_matrix(

        y_test,

        prediction

    )

)

# =====================================================
# SAVE MODEL
# =====================================================

joblib.dump(

    model,

    MODEL_PATH

)

joblib.dump(

    vectorizer,

    VECTORIZER_PATH

)

print("\nModel Saved Successfully")

print(MODEL_PATH)

print(VECTORIZER_PATH)
