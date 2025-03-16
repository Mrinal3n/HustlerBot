import os
from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langserve import add_routes
import uvicorn
from langchain_community.llms import Ollama
from dotenv import load_dotenv
from PyPDF2 import PdfReader

# Load environment variables
load_dotenv()

# Initialize the FastAPI app
app = FastAPI(
    title="HustlerBot Hostee",
    version="6.9",
    description="Hustling in mid-air"
)

# Initialize the Ollama LLM model
llm = Ollama(model="llama2")

# Define a function to read and extract text from all PDFs in the 'data' folder
def read_pdfs_from_folder(folder_path):
    pdf_texts = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, file_name)
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            pdf_texts.append(text)
    return "\n\n".join(pdf_texts)

# Set up the folder path to the 'data' folder
data_folder = os.path.join(os.getcwd(), "data")

# Extract all the text from the PDFs in the folder
pdf_content = read_pdfs_from_folder(data_folder)

# Define the ChatPromptTemplate to generate responses from the PDF content
prompt = ChatPromptTemplate.from_template("Based on the following content:\n{content}\n\nRespond elaborately about {college} in over 500 words.")

# Combine the prompt and LLM
add_routes(
    app,
    prompt | llm,
    path="/data"
)

# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
