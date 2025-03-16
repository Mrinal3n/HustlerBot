import requests
import streamlit as st

def get_ollama_response(input_text):
    response=requests.post(
    "http://localhost:8000/data/invoke",
    json={'input':{'college':input_text}})

    return response.json()['output']

st.title('Hustler Bot User Interface')
input_text=st.text_input("Give the name of the college here!")

if input_text:
    st.write(get_ollama_response(input_text))