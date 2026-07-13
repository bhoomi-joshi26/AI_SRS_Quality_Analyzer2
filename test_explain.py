from analyzer.explain_ai import explain_prediction


text = """

The system shall generate monthly reports
within 5 seconds using secure database storage.

"""


result = explain_prediction(text)


print(result)