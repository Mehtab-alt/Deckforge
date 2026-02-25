import os
from langchain_openai import ChatOpenAI

def get_llm(json_mode=False):
    model_kwargs = {"response_format": {"type": "json_object"}} if json_mode else {}
    return ChatOpenAI(
        model="gpt-4-turbo", 
        temperature=0, 
        api_key=os.getenv("OPENAI_API_KEY"),
        model_kwargs=model_kwargs
    )