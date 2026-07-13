import os
import joblib
import numpy as np



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



model = joblib.load(
    MODEL_PATH
)


vectorizer = joblib.load(
    VECTORIZER_PATH
)





# =====================================
# EXPLAIN PREDICTION
# =====================================

def explain_prediction(text):


    # Convert text to TF-IDF

    vector = vectorizer.transform(
        [text]
    )


    prediction = model.predict(
        vector
    )[0]


    probability = model.predict_proba(
        vector
    )[0]


    confidence = max(probability) * 100



    # Feature names

    feature_names = np.array(
        vectorizer.get_feature_names_out()
    )


    values = vector.toarray()[0]



    # Sort important words

    indices = np.argsort(values)[::-1]



    important_words = []


    for index in indices[:10]:


        if values[index] > 0:

            important_words.append(

                feature_names[index]

            )




    # Positive and negative explanation


    if prediction == "High":


        positive_features = important_words


        negative_features = [

            "few ambiguous terms",

            "clear requirement statements"

        ]



        message = (

            "The SRS is classified as High Quality "
            "because it contains clear requirement "
            "patterns and specific terms."

        )



    else:


        negative_features = important_words


        positive_features = [

            "some requirement keywords detected"

        ]


        message = (

            "The SRS is classified as Low Quality "
            "because it contains vague or incomplete "
            "requirement descriptions."

        )




    return {


        "prediction": prediction,


        "confidence": round(
            confidence,
            2
        ),


        "important_keywords":
            important_words,


        "positive_features":
            positive_features,


        "negative_features":
            negative_features,


        "explanation":
            message

    }