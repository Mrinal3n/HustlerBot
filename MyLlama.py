from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def update_chat_history(role, content):
    st.session_state.chat_history.append((role, content))

def build_prompt(history, user_input):
    messages = [("system", "You are Hustler Bot created by an esteemed Programmer named Mrinal from India. Please respond to the user queries.")]
    for role, content in history:
        messages.append((role, content))
    messages.append(("user", f"Question: {user_input}"))
    return ChatPromptTemplate.from_messages(messages)

st.title('Hustler Bot User Interface')
input_text = st.text_input("Pour your thoughts here!")

llm = Ollama(model="llama2")
output_parser = StrOutputParser()

if input_text:
    prompt = build_prompt(st.session_state.chat_history, input_text)
    chain = prompt | llm | output_parser
    response = chain.invoke({"question": input_text})
    update_chat_history("user", input_text)
    update_chat_history("assistant", response)
    st.write(response)

st.write("Chat History:")
for role, content in st.session_state.chat_history:
    st.write(f"**{role.capitalize()}:** {content}")
