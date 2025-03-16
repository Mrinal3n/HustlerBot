from fastapi import FastAPI
from pydantic import BaseModel
from langchain.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from pdf_loader import extract_text_from_pdfs


pdf_texts = extract_text_from_pdfs()
llm = Ollama(model="llama3.1")

def generate_llama_response(query, pdf_texts):
    """
    Generates a response using the LLaMA model by analyzing the PDF content.
    :param query: The user's query string.
    :param pdf_texts: A dictionary of PDF file names and their extracted texts.
    :return: The generated response from the LLaMA model.
    """
    combined_pdf_text = "\n\n".join([f"From {filename}:\n{content}" for filename, content in pdf_texts.items()])
    
    prompt = ChatPromptTemplate.from_template(f"""
    You are an AI assistant named Hustler Bot created by Mrinal, an elite coder of SIT. Give a welcome message regarding the same everytime. You are trained on a large dataset of PDFs.
    The user has provided the following query: "{query}"
    
    Based on the content of the PDFs, generate a detailed, over 500-word response.
    
    Content from the PDFs:
    {combined_pdf_text}
    
    Please analyze and respond based on the content of the PDFs.
    """)

    response = llm(prompt.format_prompt(query=query).to_string())
    
    return response

app = FastAPI(
    title="HustlerBot PDF Hostee with LLaMA 3.1",
    version="6.9",
    description="Hustling in mid-air, now with PDF knowledge and LLaMA 3.1!"
)

class Query(BaseModel):
    question: str

@app.post("/data/invoke")
def get_pdf_response(query: Query):
    """
    Endpoint to get responses from the PDFs based on the user's question.
    """
    input_text = query.question
    response = generate_llama_response(input_text, pdf_texts)
    return {"output": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
