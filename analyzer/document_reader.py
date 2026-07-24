import os

import re

import PyPDF2

from docx import Document
# =====================================================
# CLEAN TEXT
# =====================================================

def clean_text(text):

    if text is None:

        return ""

    # Remove multiple spaces

    text = re.sub(r"[ \t]+", " ", text)

    # Remove multiple blank lines

    text = re.sub(r"\n\s*\n+", "\n", text)

    return text.strip()
    # =====================================================
# READ PDF
# =====================================================

def read_pdf(file_path):

    text = ""

    try:

        with open(file_path, "rb") as pdf_file:

            reader = PyPDF2.PdfReader(pdf_file)

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:

                    text += page_text + "\n"

    except Exception as e:

        print("PDF Read Error :", e)

    return clean_text(text)


# =====================================================
# READ DOCX
# =====================================================

def read_docx(file_path):

    text = ""

    try:

        document = Document(file_path)

        for paragraph in document.paragraphs:

            text += paragraph.text + "\n"

    except Exception as e:

        print("DOCX Read Error :", e)

    return clean_text(text)
    # =====================================================
# READ TXT
# =====================================================

def read_txt(file_path):

    try:

        with open(

            file_path,

            "r",

            encoding="utf-8",

            errors="ignore"

        ) as file:

            return clean_text(file.read())

    except Exception as e:

        print("TXT Read Error :", e)

        return ""


# =====================================================
# MAIN DOCUMENT READER
# =====================================================

def read_document(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":

        return read_pdf(file_path)

    elif extension == ".docx":

        return read_docx(file_path)

    elif extension == ".txt":

        return read_txt(file_path)

    else:

        print("Unsupported file format.")

        return ""
