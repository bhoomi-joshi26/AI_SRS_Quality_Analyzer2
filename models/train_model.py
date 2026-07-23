import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.svm import LinearSVC

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)



# =====================================
# PATH CONFIGURATION
# =====================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


DATASET_PATH = os.path.join(
    BASE_DIR,
    "..",
    "dataset",
    "srs_dataset.csv"
)


MODEL_PATH = os.path.join(
    BASE_DIR,
    "model.pkl"
)


VECTORIZER_PATH = os.path.join(
    BASE_DIR,
    "vectorizer.pkl"
)



# =====================================
# LOAD DATASET
# =====================================

print("\nLoading SRS Dataset...")


data = pd.read_csv(
    DATASET_PATH
)


print("\nDataset Information")
print("-------------------")

print(data.head())

print("\nTotal Samples:")
print(len(data))



# Remove empty values

data.dropna(
    inplace=True
)



# Remove duplicates

data.drop_duplicates(
    subset="requirement",
    inplace=True
)



print(
    "\nDataset after cleaning:",
    len(data)
)



# =====================================
# INPUT AND OUTPUT
# =====================================

X = data["requirement"]

y = data["label"]



# =====================================
# TRAIN TEST SPLIT
# =====================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)



print("\nTraining Samples:")
print(len(X_train))


print("Testing Samples:")
print(len(X_test))



# =====================================
# TF-IDF FEATURE EXTRACTION
# =====================================

print("\nConverting Text into Numerical Features...")


vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    max_features=10000,
    ngram_range=(1,2),
    sublinear_tf=True,
    min_df=2,
    max_df=0.95
)



X_train_vector = vectorizer.fit_transform(
    X_train
)


X_test_vector = vectorizer.transform(
    X_test
)



print(
    "Feature Count:",
    len(vectorizer.get_feature_names_out())
)



# =====================================
# MACHINE LEARNING MODEL
# =====================================

print("\nTraining Random Forest Model...")


model = LinearSVC(
    class_weight="balanced",
    random_state=42
)



model.fit(

    X_train_vector,

    y_train

)



# =====================================
# MODEL TESTING
# =====================================

print("\nTesting Model...")


prediction = model.predict(

    X_test_vector

)



accuracy = accuracy_score(

    y_test,

    prediction

)



print("\n============================")
print("MODEL PERFORMANCE")
print("============================")


print(
    "Accuracy:",
    round(
        accuracy*100,
        2
    ),
    "%"
)



print("\nClassification Report:")


print(

    classification_report(

        y_test,

        prediction

    )

)



print("\nConfusion Matrix:")


print(

    confusion_matrix(

        y_test,

        prediction

    )

)



# =====================================
# SAVE MODEL
# =====================================


joblib.dump(

    model,

    MODEL_PATH

)



joblib.dump(

    vectorizer,

    VECTORIZER_PATH

)



print("\n============================")
print("TRAINING COMPLETED")
print("============================")


print(
    "Model Saved:",
    MODEL_PATH
)


print(
    "Vectorizer Saved:",
    VECTORIZER_PATH
)