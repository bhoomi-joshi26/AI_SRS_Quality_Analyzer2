from analyzer.quality_checker import analyze_srs



text = """

The system shall allow users 
to login using password authentication.

The application should be fast 
and easy to use.

"""


result = analyze_srs(text)


print(result)