import streamlit as st
from langchain.llms import Ollama  # Assuming you're using the Ollama LLaMA 3.1 model
from langchain.prompts import ChatPromptTemplate
from pdf_loader import extract_text_from_pdfs  # Import the PDF loader function

# Load the PDF texts
pdf_texts = extract_text_from_pdfs()

# Initialize LLaMA 3.1 model (assuming Ollama or similar backend is running locally)
llm = Ollama(model="llama3.1")

# Define the function to generate responses using LLaMA 3.1
def generate_llama_response(query, pdf_texts):
    """
    Generates a response using the LLaMA model by analyzing the PDF content.
    :param query: The user's query string.
    :param pdf_texts: A dictionary of PDF file names and their extracted texts.
    :return: The generated response from the LLaMA model.
    """
    # Concatenate all PDF text to feed into the LLM prompt
    combined_pdf_text = "\n\n".join([f"From {filename}:\n{content}" for filename, content in pdf_texts.items()])
    
    # Create a prompt template to send to the LLaMA model
    prompt = ChatPromptTemplate.from_template(f"""
    You are an AI assistant trained on a large dataset of PDFs.
    The user has provided the following query: "{query}"
    
    Based on the content of the PDFs, generate a detailed, over 500-word response.
    
    Content from the PDFs:
    {combined_pdf_text}
    
    Please analyze and respond based on the content of the PDFs.
    """)

    # Get the response from the LLaMA model
    response = llm(prompt.format_prompt(query=query).to_string())
    
    return response

# Streamlit Interface
st.title('Hustler Bot PDF Interface with LLaMA 3.1')

input_text = st.text_input("Ask a question about the content in the PDFs")

if input_text:
    response = generate_llama_response(input_text, pdf_texts)
    st.write(response)
