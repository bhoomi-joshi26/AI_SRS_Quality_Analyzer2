from analyzer.document_reader import read_document


file_path = "sample_documents/sample_srs.txt"


text = read_document(file_path)


print(text)