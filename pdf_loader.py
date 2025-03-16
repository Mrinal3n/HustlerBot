import os
import pdfplumber

def extract_text_from_pdfs(directory="data"):
    """
    Extracts text from all PDFs in the given directory.
    :param directory: Directory containing PDF files.
    :return: A dictionary where keys are file names and values are the content of the PDFs.
    """
    pdf_texts = {}
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            with pdfplumber.open(os.path.join(directory, filename)) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text()
                pdf_texts[filename] = text
    return pdf_texts
if __name__ == "__main__":
    pdf_texts = extract_text_from_pdfs()
    print(pdf_texts)
