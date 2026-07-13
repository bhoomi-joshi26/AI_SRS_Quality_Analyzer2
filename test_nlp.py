from analyzer.nlp_processor import preprocess_text


text = """
The system shall allow users
to login using username and password.
"""


result = preprocess_text(text)


print(result)