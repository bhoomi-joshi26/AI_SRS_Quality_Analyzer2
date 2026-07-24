import os
import re
import joblib
import numpy as np

# =====================================================
# PROJECT PATHS
# =====================================================

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

# =====================================================
# LOAD MODEL
# =====================================================

model = joblib.load(MODEL_PATH)

vectorizer = joblib.load(VECTORIZER_PATH)
# =====================================================
# CONFIGURATION
# =====================================================

AMBIGUOUS_WORDS = [

    "fast",
    "quick",
    "easy",
    "simple",
    "good",
    "better",
    "efficient",
    "proper",
    "many",
    "large",
    "soon",
    "etc",
    "appropriate",
    "sufficient",
    "user friendly"

]

POSITIVE_KEYWORDS = [

    "shall",
    "authentication",
    "security",
    "performance",
    "encryption",
    "password",
    "otp",
    "access",
    "login",
    "logout",
    "search",
    "upload",
    "download",
    "store",
    "process",
    "generate",
    "manage",
    "response",
    "reliability",
    "availability"

]


# =====================================================
# EXPLAIN PREDICTION
# =====================================================

def explain_prediction(text):

    vector = vectorizer.transform([text])

    prediction = model.predict(vector)[0]

    probability = model.predict_proba(vector)[0]

    confidence = round(max(probability) * 100, 2)

    feature_names = np.array(
        vectorizer.get_feature_names_out()
    )

    values = vector.toarray()[0]

    indices = np.argsort(values)[::-1]

    important_words = []

    for index in indices:

        if values[index] <= 0:
            continue

        important_words.append(
            feature_names[index]
        )

        if len(important_words) == 15:
            break
                # =====================================================
    # POSITIVE INDICATORS
    # =====================================================

    positive_features = []

    for word in important_words:

        if word.lower() in POSITIVE_KEYWORDS:

            positive_features.append(word)

    # =====================================================
    # NEGATIVE INDICATORS
    # =====================================================

    negative_features = []

    text_lower = text.lower()

    for word in AMBIGUOUS_WORDS:

        if re.search(r"\b" + re.escape(word) + r"\b", text_lower):

            negative_features.append(word)

    # If no positive keywords were found,
    # show the most important TF-IDF words

    if len(positive_features) == 0:

        positive_features = important_words[:5]

    # Remove duplicate entries

    positive_features = list(dict.fromkeys(positive_features))

    negative_features = list(dict.fromkeys(negative_features))
        # =====================================================
    # EXPLANATION MESSAGE
    # =====================================================

    if prediction == "High":

        explanation = (
            "The uploaded SRS is classified as High Quality because "
            "it contains clear, structured and measurable requirement "
            "statements with appropriate software engineering terminology."
        )

    else:

        explanation = (
            "The uploaded SRS is classified as Low Quality because "
            "it contains ambiguous, incomplete or poorly specified "
            "requirements that may lead to software defects."
        )

    # If there are no negative indicators, don't invent any

    if len(negative_features) == 0:

        negative_features = []

    # If there are no positive indicators, show the most
    # important keywords extracted by TF-IDF

    if len(positive_features) == 0:

        positive_features = important_words[:5]

    # =====================================================
    # RETURN RESULT
    # =====================================================

    return {

        "prediction": prediction,

        "confidence": confidence,

        "important_keywords": important_words,

        "positive_features": positive_features,

        "negative_features": negative_features,

        "explanation": explanation

    }
            
