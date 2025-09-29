from fastapi import FastAPI
from pydantic import BaseModel
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_community.llms import Ollama  # Change to use Ollama
from dotenv import load_dotenv
import os
import google.generativeai as genai
import requests

# Load environment variables
load_dotenv()

def parseApiKey() -> str:
    """
    Safely retrieve the API key from environment variables.
    Returns:
        str: The API key if found, or None if not found
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    return api_key

api_key = parseApiKey()

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash")

thread = model.start_chat()

response = thread.send_message("Hello, what do you do?")

print(response)




