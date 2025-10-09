from fastapi import FastAPI
from dotenv import load_dotenv
from datetime import datetime
import os
import sys
import google.generativeai as genai
import requests

# Add the physics-gemini directory to Python path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

# Now we can import directly from the local modules
from prompting.promptLoader import PromptLoader
import services.database as db

# Initialize Database
db.init_db() 

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

def update_markdown(question: str, response_text: str):
    """Update the physics_responses.md file with the latest Q&A"""
    markdown_path = os.path.join(project_dir, "responses", "physics_responses.md")
    
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    markdown_content = f"""# Physics Q&A Session - {timestamp}

## Question
{question}

## Response
{response_text}

---
"""
    # Write the new content to the file
    with open(markdown_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

# Gemini API Key
api_key = parseApiKey()

# LLM configuation and initialization
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")
thread = model.start_chat()

pl = PromptLoader()
prompt = pl.load_prompt("core_physics_prompt")

# Initial question
user_question = input("Enter your physics question as text: ")

# Main interaction loop
while user_question != "quit":
    formatted_prompt = prompt.replace("{question}", user_question)

    # Print the formatted prompt for debugging
    print("\nSending prompt to Gemini:")
    print("\nWaiting for response...")

    response = thread.send_message(formatted_prompt)
    print(f"Response from Gemini:\n{response.text}")
    
    # Update the markdown file with the latest response
    update_markdown(user_question, response.text)
    
    # TODO: Store in database
    db.add_response(user_question, response.text)

    # Continue loop
    user_question = input("\nEnter your physics question as text (or 'quit' to exit): ")
