import os
import joblib
import re



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

    model = joblib.load(
        MODEL_PATH
    )


    vectorizer = joblib.load(
        VECTORIZER_PATH
    )


except Exception as e:

    print(
        "Model loading error:",
        e
    )





# ==========================================
# AMBIGUOUS WORD DETECTION
# ==========================================

ambiguous_words = [

    "fast",
    "quick",
    "easy",
    "simple",
    "better",
    "good",
    "efficient",
    "proper",
    "user friendly",
    "soon",
    "large",
    "many",
    "high"

]





def detect_ambiguity(text):


    found = []


    text = text.lower()



    for word in ambiguous_words:


        if word in text:


            found.append(
                word
            )


    return found





# ==========================================
# REQUIREMENT STATISTICS
# ==========================================

def requirement_statistics(text):


    sentences = re.split(

        r'[.!?]', 

        text

    )


    requirements = []


    for sentence in sentences:


        if len(sentence.strip()) > 10:


            requirements.append(
                sentence.strip()
            )



    total = len(
        requirements
    )



    functional = 0

    non_functional = 0



    keywords_functional = [

        "shall",
        "allow",
        "provide",
        "generate",
        "store",
        "process"

    ]



    keywords_nonfunctional = [

        "security",
        "performance",
        "availability",
        "reliability",
        "response time"

    ]



    for req in requirements:


        req = req.lower()



        if any(
            word in req
            for word in keywords_functional
        ):

            functional += 1



        if any(
            word in req
            for word in keywords_nonfunctional
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

        score += 20



    else:

        score -= 20



    score -= ambiguity_count * 3



    score = max(
        0,
        min(
            score,
            100
        )
    )



    return round(
        score,
        2
    )





# ==========================================
# MAIN ANALYZER FUNCTION
# ==========================================

def analyze_srs(text):


    if model is None:


        return {

            "error":
            "Model not available"

        }



    # Convert text into features

    vector = vectorizer.transform(

        [text]

    )



    prediction = model.predict(

        vector

    )[0]



    probability = model.predict_proba(

        vector

    )[0]



    confidence = max(
        probability
    ) * 100



    ambiguity = detect_ambiguity(

        text

    )



    statistics = requirement_statistics(

        text

    )



    quality_score = calculate_quality_score(

        prediction,

        confidence,

        len(ambiguity)

    )





    if prediction == "High":


        message = (

            "The SRS contains clear and "
            "well-defined requirements."

        )


        suggestions = []


    else:


        message = (

            "The SRS contains unclear or "
            "ambiguous requirements."

        )


        suggestions = [

            "Avoid vague words like fast, easy, better",

            "Add measurable values and constraints",

            "Specify functional and non-functional requirements",

            "Define expected system behavior clearly"

        ]





    return {


        "prediction": prediction,


        "confidence": round(
            confidence,
            2
        ),


        "quality_score": quality_score,


        "message": message,


        "ambiguous_words": ambiguity,


        "statistics": statistics,


        "suggestions": suggestions

    }