from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langserve import add_routes
import uvicorn
import os
from langchain_community.llms import Ollama
from dotenv import load_dotenv

load_dotenv()

app=FastAPI(
    title="HustlerBot Hostee",
    version="6.9",
    description="Hustling in mid-air"

)

llm=Ollama(model="llama2")

prompt=ChatPromptTemplate.from_template("Elaborately give all the details about {college} in over 500 words")

add_routes(
    app,
    prompt|llm,
    path="/data"
)

if __name__=="__main__":
    uvicorn.run(app,host="localhost",port=8000)