import os
import re
import joblib

# ==========================================
# MODEL PATH
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

except Exception as e:

    print("Model Loading Error :", e)

# ==========================================
# IMPROVED AMBIGUOUS WORDS
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
    "soon",
    "etc",
    "and so on",
    "appropriate",
    "sufficient"

]

# ==========================================
# DETECT AMBIGUITY
# ==========================================

def detect_ambiguity(text):

    text = text.lower()

    found = []

    for word in AMBIGUOUS_WORDS:

        pattern = r"\b" + re.escape(word) + r"\b"

        if re.search(pattern, text):

            found.append(word)

    return sorted(list(set(found)))
# ==========================================
# REQUIREMENT STATISTICS
# ==========================================

def requirement_statistics(text):

    # Split text into individual requirements
    requirements = []

    sentences = re.split(r"[.!?\n]+", text)

    for sentence in sentences:

        sentence = sentence.strip()

        if len(sentence) > 10:

            requirements.append(sentence)

    total_requirements = len(requirements)

    functional = 0
    non_functional = 0

    # Functional requirement keywords
    functional_keywords = [

        "shall",
        "allow",
        "login",
        "log in",
        "register",
        "generate",
        "update",
        "delete",
        "insert",
        "search",
        "upload",
        "download",
        "process",
        "store",
        "create",
        "manage",
        "book",
        "track",
        "calculate",
        "display"

    ]

    # Non-functional requirement keywords
    nonfunctional_keywords = [

        "performance",
        "security",
        "response time",
        "availability",
        "reliability",
        "encryption",
        "authentication",
        "authorization",
        "latency",
        "backup",
        "recovery",
        "maintainability",
        "scalability",
        "confidentiality",
        "integrity",
        "usability",
        "access control",
        "aes",
        "otp",
        "multi factor",
        "role based"

    ]

    for req in requirements:

        req = req.lower()

        # Functional Requirement
        if any(keyword in req for keyword in functional_keywords):

            functional += 1

        # Non Functional Requirement
        if any(keyword in req for keyword in nonfunctional_keywords):

            non_functional += 1

    # Prevent impossible values
    functional = min(functional, total_requirements)
    non_functional = min(non_functional, total_requirements)

    return {

        "total_requirements": total_requirements,

        "functional_requirements": functional,

        "non_functional_requirements": non_functional

    }
# ==========================================
# QUALITY SCORE CALCULATION
# ==========================================

def calculate_quality_score(text, prediction, confidence, ambiguity_count):

    text = text.lower()

    score = 100

    # --------------------------------------
    # Penalize Ambiguous Words
    # --------------------------------------

    score -= ambiguity_count * 5

    # --------------------------------------
    # Mandatory Requirement Keyword
    # --------------------------------------

    if "shall" not in text:
        score -= 10

    # --------------------------------------
    # Measurable Values
    # --------------------------------------

    measurable_patterns = [

        r"\d+\s*second",
        r"\d+\s*seconds",
        r"\d+\s*minute",
        r"\d+\s*minutes",
        r"\d+\s*ms",
        r"\d+\s*%",
        r"\d+\s*mb",
        r"\d+\s*gb"

    ]

    measurable_found = False

    for pattern in measurable_patterns:

        if re.search(pattern, text):

            measurable_found = True
            break

    if not measurable_found:
        score -= 10

    # --------------------------------------
    # Actor Detection
    # --------------------------------------

    actors = [

        "user",
        "customer",
        "administrator",
        "employee",
        "system operator",
        "registered user"

    ]

    if not any(actor in text for actor in actors):

        score -= 5

    # --------------------------------------
    # Action Detection
    # --------------------------------------

    actions = [

        "login",
        "log in",
        "upload",
        "download",
        "search",
        "generate",
        "update",
        "delete",
        "store",
        "process",
        "manage",
        "track",
        "create"

    ]

    if not any(action in text for action in actions):

        score -= 5

    # --------------------------------------
    # Security Requirement
    # --------------------------------------

    security_keywords = [

        "aes",
        "encryption",
        "encrypted",
        "otp",
        "authentication",
        "authorization",
        "role based",
        "access control",
        "password",
        "secure"

    ]

    if any(word in text for word in security_keywords):

        score += 5

    # --------------------------------------
    # Performance Requirement
    # --------------------------------------

    performance_keywords = [

        "response time",
        "within",
        "performance"

    ]

    if any(word in text for word in performance_keywords):

        score += 5

    # --------------------------------------
    # ML Confidence Adjustment
    # --------------------------------------

    if prediction == "High":

        score += (confidence * 0.05)

    else:

        score -= (100 - confidence) * 0.05

    # --------------------------------------
    # Limit Score
    # --------------------------------------

    score = max(0, min(score, 100))

    return round(score, 2)
# ==========================================
# MAIN SRS ANALYZER
# ==========================================

def analyze_srs(text):

    if model is None or vectorizer is None:

        return {
            "error": "Model not available"
        }

    # --------------------------------------
    # Convert Text into TF-IDF Features
    # --------------------------------------

    vector = vectorizer.transform([text])

    prediction = model.predict(vector)[0]

    # --------------------------------------
    # Confidence Score
    # --------------------------------------

    if hasattr(model, "predict_proba"):

        probability = model.predict_proba(vector)[0]
        confidence = round(max(probability) * 100, 2)

    else:

        confidence = 85.00

    # --------------------------------------
    # Ambiguity Detection
    # --------------------------------------

    ambiguity = detect_ambiguity(text)

    # --------------------------------------
    # Requirement Statistics
    # --------------------------------------

    statistics = requirement_statistics(text)

    # --------------------------------------
    # Quality Score
    # --------------------------------------

    quality_score = calculate_quality_score(
        text,
        prediction,
        confidence,
        len(ambiguity)
    )

    # --------------------------------------
    # Dynamic Assessment Message
    # --------------------------------------

    if quality_score >= 85:

        message = (
            "Excellent SRS. Requirements are clear, "
            "measurable and well structured."
        )

    elif quality_score >= 70:

        message = (
            "Good SRS with minor improvements required."
        )

    elif quality_score >= 50:

        message = (
            "Average SRS. Several requirements need "
            "clarification."
        )

    else:

        message = (
            "Poor SRS. Requirements contain ambiguity "
            "and should be rewritten."
        )

    # --------------------------------------
    # Improvement Suggestions
    # --------------------------------------

    suggestions = []

    if ambiguity:

        suggestions.append(
            "Replace ambiguous words with measurable terms."
        )

    if "shall" not in text.lower():

        suggestions.append(
            "Use 'shall' instead of 'should' for mandatory requirements."
        )

    if not re.search(
        r"\d+\s*(second|seconds|minute|minutes|ms|%)",
        text.lower()
    ):

        suggestions.append(
            "Add measurable values such as response time or limits."
        )

    security_keywords = [
        "authentication",
        "authorization",
        "password",
        "otp",
        "aes",
        "secure",
        "access control",
        "encryption"
    ]

    if not any(word in text.lower() for word in security_keywords):

        suggestions.append(
            "Specify security requirements where applicable."
        )

    actors = [
        "user",
        "customer",
        "administrator",
        "employee",
        "system operator",
        "registered user"
    ]

    if not any(actor in text.lower() for actor in actors):

        suggestions.append(
            "Clearly identify the actor performing the action."
        )

    if len(suggestions) == 0:

        suggestions.append(
            "Your SRS follows good software engineering practices."
        )

    # --------------------------------------
    # Return Results
    # --------------------------------------

    return {

        "prediction": prediction,

        "confidence": confidence,

        "quality_score": quality_score,

        "message": message,

        "ambiguous_words": ambiguity,

        "statistics": statistics,

        "suggestions": suggestions

    }