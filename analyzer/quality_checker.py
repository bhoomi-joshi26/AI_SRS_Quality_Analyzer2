import os
import re
import joblib

# ==========================================
# PROJECT PATHS
# ==========================================

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

# ==========================================
# LOAD MODEL
# ==========================================

model = None
vectorizer = None

try:

    model = joblib.load(MODEL_PATH)

    vectorizer = joblib.load(VECTORIZER_PATH)

    print("✅ Model Loaded Successfully")

except Exception as e:

    print("❌ Model Loading Error:", e)

# ==========================================
# CONFIGURATION
# ==========================================

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

FUNCTIONAL_KEYWORDS = [

    "shall",
    "allow",
    "login",
    "logout",
    "register",
    "search",
    "upload",
    "download",
    "create",
    "delete",
    "update",
    "store",
    "process",
    "track",
    "generate",
    "manage",
    "view",
    "edit",
    "authenticate",
    "verify",
    "notify"

]

NON_FUNCTIONAL_KEYWORDS = [

    "security",
    "performance",
    "response time",
    "availability",
    "reliability",
    "scalability",
    "usability",
    "maintainability",
    "latency",
    "aes",
    "encryption",
    "encrypted",
    "otp",
    "password",
    "authentication",
    "access control",
    "backup",
    "recovery",
    "seconds",
    "second",
    "ms",
    "database",
    "secure"

]
# ==========================================
# AMBIGUITY DETECTION
# ==========================================

def detect_ambiguity(text):

    found = []

    text = text.lower()

    for word in AMBIGUOUS_WORDS:

        if re.search(r"\b" + re.escape(word) + r"\b", text):

            found.append(word)

    return sorted(list(set(found)))


# ==========================================
# EXTRACT REQUIREMENTS
# ==========================================

def extract_requirements(text):

    text = text.replace("\r", "\n")

    requirements = []

    REQUIREMENT_WORDS = [

        "shall",
        "should",
        "must",
        "will",
        "allow",
        "provide",
        "system"

    ]

    for line in text.split("\n"):

        line = line.strip()

        if len(line) < 10:

            continue

        lower = line.lower()

        if any(word in lower for word in REQUIREMENT_WORDS):

            requirements.append(line)

    return requirements


# ==========================================
# REQUIREMENT STATISTICS
# ==========================================

def requirement_statistics(text):

    requirements = extract_requirements(text)

    total = len(requirements)

    functional = 0

    non_functional = 0

    for req in requirements:

        req_lower = req.lower()

        if any(
            re.search(r"\b" + re.escape(word) + r"\b", req_lower)
            for word in FUNCTIONAL_KEYWORDS
        ):

            functional += 1

        if any(
            re.search(r"\b" + re.escape(word) + r"\b", req_lower)
            for word in NON_FUNCTIONAL_KEYWORDS
        ):

            non_functional += 1

    return {

        "total_requirements": total,

        "functional_requirements": functional,

        "non_functional_requirements": non_functional

    }
# ==========================================
# QUALITY SCORE
# ==========================================

def calculate_quality_score(

        prediction,

        confidence,

        ambiguity_count

):

    score = confidence

    if prediction == "High":

        score += 10

    else:

        score -= 10

    # Deduct marks for ambiguous words
    score -= ambiguity_count * 5

    score = max(0, min(score, 100))

    return round(score, 2)


# ==========================================
# MAIN ANALYZER
# ==========================================

def analyze_srs(processed_text, original_text):

    if model is None or vectorizer is None:

        return {

            "prediction": "Unknown",

            "confidence": 0,

            "quality_score": 0,

            "message": "Model not loaded.",

            "ambiguous_words": [],

            "statistics": {},

            "suggestions": []

        }

    # ------------------------------
    # ML Prediction
    # ------------------------------

    vector = vectorizer.transform([processed_text])

    prediction = model.predict(vector)[0]

    probability = model.predict_proba(vector)[0]

    confidence = round(max(probability) * 100, 2)

    # ------------------------------
    # Rule-Based Analysis
    # ------------------------------

    ambiguity = detect_ambiguity(original_text)

    statistics = requirement_statistics(original_text.strip())

    quality_score = calculate_quality_score(

        prediction,

        confidence,

        len(ambiguity)

    )

    # ------------------------------
    # Message
    # ------------------------------

    if prediction == "High":

        message = (
            "The SRS contains clear, measurable and "
            "well-structured requirements."
        )

    else:

        message = (
            "The SRS contains ambiguous or "
            "poorly specified requirements."
        )

    suggestions = []# ==========================================
# MAIN ANALYZER
# ==========================================

def analyze_srs(processed_text, original_text):

    if model is None or vectorizer is None:

        return {

            "prediction": "Unknown",
            "confidence": 0,
            "quality_score": 0,
            "message": "Model not loaded.",
            "ambiguous_words": [],
            "statistics": {},
            "suggestions": []

        }

    # -----------------------------
    # Machine Learning Prediction
    # -----------------------------

    vector = vectorizer.transform([processed_text])

    prediction = model.predict(vector)[0]

    probability = model.predict_proba(vector)[0]

    confidence = round(max(probability) * 100, 2)

    # -----------------------------
    # Rule-based Analysis
    # -----------------------------

    ambiguity = detect_ambiguity(original_text)

    statistics = requirement_statistics(original_text)

    quality_score = calculate_quality_score(
        prediction,
        confidence,
        len(ambiguity)
    )

    # -----------------------------
    # Message
    # -----------------------------

    if prediction == "High":

        message = (
            "The uploaded SRS is well structured and "
            "contains clear, measurable requirements."
        )

    else:

        message = (
            "The uploaded SRS contains vague or "
            "incomplete requirements."
        )

    # -----------------------------
    # Suggestions
    # -----------------------------

    suggestions = []

    if ambiguity:

        suggestions.append(
            "Remove ambiguous words: "
            + ", ".join(ambiguity)
        )

    if statistics["functional_requirements"] == 0:

        suggestions.append(
            "Add functional requirements using words like 'shall', 'login', 'process', 'store' etc."
        )

    if statistics["non_functional_requirements"] == 0:

        suggestions.append(
            "Include measurable non-functional requirements such as performance, security, reliability and response time."
        )

    if not re.search(
        r"\b\d+\s*(second|seconds|ms|minute|minutes)\b",
        original_text.lower()
    ):

        suggestions.append(
            "Specify measurable constraints (example: response time within 2 seconds)."
        )

    if "shall" not in original_text.lower():

        suggestions.append(
            "Prefer 'shall' instead of 'should' in mandatory requirements."
        )

    if not suggestions:

        suggestions.append(
            "Excellent SRS. No major improvements required."
        )

    # -----------------------------
    # Return Result
    # -----------------------------

    return {

        "prediction": prediction,

        "confidence": confidence,

        "quality_score": quality_score,

        "message": message,

        "ambiguous_words": ambiguity,

        "statistics": statistics,

        "suggestions": suggestions

    }
