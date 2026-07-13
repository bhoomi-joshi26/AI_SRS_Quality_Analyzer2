import os

from PyPDF2 import PdfReader

from docx import Document



# =========================================
# READ TEXT FILE
# =========================================

def read_txt(file_path):

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read()


        return text


    except Exception as e:

        return f"Error reading TXT file: {e}"




# =========================================
# READ PDF FILE
# =========================================

def read_pdf(file_path):

    try:

        reader = PdfReader(
            file_path
        )


        text = ""


        for page in reader.pages:

            page_text = page.extract_text()


            if page_text:

                text += page_text + "\n"



        return text



    except Exception as e:

        return f"Error reading PDF file: {e}"




# =========================================
# READ DOCX FILE
# =========================================

def read_docx(file_path):

    try:

        document = Document(
            file_path
        )


        text = ""


        for paragraph in document.paragraphs:

            text += paragraph.text + "\n"



        return text



    except Exception as e:

        return f"Error reading DOCX file: {e}"





# =========================================
# MAIN DOCUMENT READER FUNCTION
# =========================================

def read_document(file_path):


    if not os.path.exists(file_path):

        return "File does not exist"



    extension = os.path.splitext(
        file_path
    )[1].lower()



    if extension == ".txt":

        return read_txt(
            file_path
        )



    elif extension == ".pdf":

        return read_pdf(
            file_path
        )



    elif extension == ".docx":

        return read_docx(
            file_path
        )



    else:

        return (
            "Unsupported file format. "
            "Please upload TXT, PDF or DOCX file."
        )