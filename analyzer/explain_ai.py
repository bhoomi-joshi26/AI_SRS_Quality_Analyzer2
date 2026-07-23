import os
import re
import joblib
import numpy as np

# =====================================
# MODEL PATH
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

# =====================================
# LOAD MODEL
# =====================================

model = None
vectorizer = None

try:

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)

except Exception as e:

    print("Explain AI Model Loading Error :", e)

# =====================================
# AMBIGUOUS WORDS
# =====================================

AMBIGUOUS_WORDS = [

    "fast",
    "quick",
    "easy",
    "simple",
    "good",
    "better",
    "efficient",
    "proper",
    "user friendly",
    "friendly",
    "modern",
    "advanced",
    "robust",
    "flexible",
    "powerful",
    "acceptable",
    "adequate",
    "optimal",
    "best",
    "many",
    "large",
    "high",
    "low",
    "soon"

]

# =====================================
# DETECT AMBIGUITY
# =====================================

def detect_ambiguity(text):

    text = text.lower()

    found = []

    for word in AMBIGUOUS_WORDS:

        pattern = r"\b" + re.escape(word) + r"\b"

        if re.search(pattern, text):

            found.append(word)

    return sorted(list(set(found)))
# =====================================
# POSITIVE & NEGATIVE FEATURE ANALYSIS
# =====================================

def analyze_features(text):

    text = text.lower()

    positive_features = []
    negative_features = []

    # ---------------------------------
    # Positive Indicators
    # ---------------------------------

    if "shall" in text:
        positive_features.append(
            "Uses mandatory keyword 'shall'"
        )

    if re.search(r"\d+\s*(second|seconds|minute|minutes|ms|%)", text):
        positive_features.append(
            "Contains measurable performance requirement"
        )

    security_keywords = [

        "authentication",
        "authorization",
        "password",
        "otp",
        "aes",
        "encryption",
        "encrypted",
        "secure",
        "access control",
        "role based"

    ]

    if any(word in text for word in security_keywords):

        positive_features.append(
            "Contains security requirement"
        )

    actors = [

        "user",
        "customer",
        "administrator",
        "employee",
        "registered user",
        "system operator"

    ]

    if any(actor in text for actor in actors):

        positive_features.append(
            "Clearly identifies system actor"
        )

    actions = [

        "login",
        "log in",
        "upload",
        "download",
        "search",
        "generate",
        "process",
        "update",
        "delete",
        "store",
        "manage",
        "track",
        "create"

    ]

    if any(action in text for action in actions):

        positive_features.append(
            "Clearly specifies system action"
        )

    # ---------------------------------
    # Negative Indicators
    # ---------------------------------

    ambiguous = detect_ambiguity(text)

    for word in ambiguous:

        negative_features.append(
            f"Contains ambiguous word: '{word}'"
        )

    if "should" in text and "shall" not in text:

        negative_features.append(
            "Uses 'should' instead of 'shall'"
        )

    if not re.search(
        r"\d+\s*(second|seconds|minute|minutes|ms|%)",
        text
    ):

        negative_features.append(
            "Requirement is not measurable"
        )

    return positive_features, negative_features
# =====================================
# EXPLAIN PREDICTION
# =====================================

def explain_prediction(text):

    if model is None or vectorizer is None:

        return {

            "prediction": "Unknown",

            "confidence": 0,

            "important_keywords": [],

            "positive_features": [],

            "negative_features": [

                "Model not loaded"

            ],

            "explanation": "Explainable AI model is unavailable."

        }

    # ---------------------------------
    # TF-IDF Vector
    # ---------------------------------

    vector = vectorizer.transform([text])

    prediction = model.predict(vector)[0]

    # ---------------------------------
    # Confidence
    # ---------------------------------

    if hasattr(model, "predict_proba"):

        probability = model.predict_proba(vector)[0]

        confidence = round(max(probability) * 100, 2)

    else:

        confidence = 85.0

    # ---------------------------------
    # Important Keywords
    # ---------------------------------

    feature_names = np.array(
        vectorizer.get_feature_names_out()
    )

    values = vector.toarray()[0]

    indices = np.argsort(values)[::-1]

    important_keywords = []

    for index in indices:

        if values[index] > 0:

            important_keywords.append(
                feature_names[index]
            )

        if len(important_keywords) == 10:

            break

    # ---------------------------------
    # Dynamic Feature Analysis
    # ---------------------------------

    positive_features, negative_features = analyze_features(text)

    # ---------------------------------
    # Dynamic Explanation
    # ---------------------------------

    if prediction == "High":

        explanation = (

            "The requirement is classified as HIGH quality "

            "because it contains clear, measurable "

            "and well-structured statements."

        )

    else:

        explanation = (

            "The requirement is classified as LOW quality "

            "because it contains ambiguity or lacks "

            "clear measurable information."

        )

    return {

        "prediction": prediction,

        "confidence": confidence,

        "important_keywords": important_keywords,

        "positive_features": positive_features,

        "negative_features": negative_features,

        "explanation": explanation

    }