import os
import re
import joblib

# =====================================
# LOAD MODEL
# =====================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "model.pkl"
)

VECTORIZER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "vectorizer.pkl"
)

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

# =====================================
# KEYWORD LISTS
# =====================================

POSITIVE_KEYWORDS = [

    "shall",
    "authentication",
    "security",
    "encryption",
    "aes",
    "otp",
    "password",
    "role",
    "access control",
    "performance",
    "response time",
    "reliability",
    "availability",
    "store",
    "process",
    "generate",
    "upload",
    "download",
    "login",
    "logout",
    "database"

]

NEGATIVE_KEYWORDS = [

    "fast",
    "easy",
    "good",
    "better",
    "simple",
    "efficient",
    "proper",
    "advanced",
    "many",
    "large",
    "soon",
    "etc",
    "appropriate",
    "sufficient"

]
# =====================================
# FIND POSITIVE INDICATORS
# =====================================

def get_positive_features(text):

    text = text.lower()

    positive = []

    for word in POSITIVE_KEYWORDS:

        if re.search(r"\b" + re.escape(word) + r"\b", text):

            positive.append(word)

    return sorted(list(set(positive)))


# =====================================
# FIND NEGATIVE INDICATORS
# =====================================

def get_negative_features(text):

    text = text.lower()

    negative = []

    for word in NEGATIVE_KEYWORDS:

        if re.search(r"\b" + re.escape(word) + r"\b", text):

            negative.append(word)

    return sorted(list(set(negative)))
# =====================================
# EXPLAIN PREDICTION
# =====================================

def explain_prediction(text):

    # ML Prediction

    vector = vectorizer.transform([text])

    prediction = model.predict(vector)[0]

    probability = model.predict_proba(vector)[0]

    confidence = round(max(probability) * 100, 2)

    # Detect Indicators

    positive_features = get_positive_features(text)

    negative_features = get_negative_features(text)

    # Explanation Message

    if prediction == "High":

        explanation = (
            "The SRS is classified as High Quality because it contains "
            "clear, measurable and well-structured requirement statements."
        )

    else:

        explanation = (
            "The SRS is classified as Low Quality because it contains "
            "ambiguous, incomplete or non-measurable requirements."
        )
    # ---------------------------------
    # Default Messages
    # ---------------------------------

    if len(positive_features) == 0:

        positive_features.append(
            "No strong SRS quality indicators found."
        )

    if len(negative_features) == 0:

        negative_features.append(
            "No ambiguous words detected."
        )

    # ---------------------------------
    # Return Result
    # ---------------------------------

    return {

        "prediction": prediction,

        "confidence": confidence,

        "positive_features": positive_features,

        "negative_features": negative_features,

        "explanation": explanation

    }