from fastapi import FastAPI
from dotenv import load_dotenv
from datetime import datetime
import os
import sys
import google.generativeai as genai
import requests
import sqlite3
from database.database import Database  # Import our database handler

# Add the root directory to Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

from prompting.promptLoader import PromptLoader
sys.path.append(os.path.join(root_dir, 'database'))
from database import Database

# Initialize database
db = Database()
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
    
    # Store in database
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO responses (question, response) VALUES (?, ?)",
                (user_question, response.text)
            )
            conn.commit()
        print("\nResponse saved to database and markdown file")
    except sqlite3.Error as e:
        print(f"\nError saving to database: {e}")
        print("Response only saved to markdown file")

    user_question = input("\nEnter your physics question as text (or 'quit' to exit): ")








