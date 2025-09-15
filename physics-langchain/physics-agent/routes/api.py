from fastapi import FastAPI
from pydantic import BaseModel
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_openai import ChatOpenAI

import requests

# Agent and Tool Types
class AgentRequest(BaseModel):
    question: str

# Initialize FastAPI app
app = FastAPI(title="Physics Agent")

# LLM calling - references OPENAI_API_KEY
llm = ChatOpenAI(temperature=0, model="gpt-4")

def get_physics_answer(query: str) -> str:
    """Queries an external Physics DB API for an answer. Includes error handling."""
    # NOTE: This URL is a placeholder. Replace with a real API endpoint.
    url = f"http://api.physicsdb.com/qa?query={query}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        return response.json().get("answer", "No answer found in the database for that query.")
    except requests.exceptions.RequestException as e:
        return f"Error connecting to the physics database: {e}"
    except ValueError:  # Catches JSON decoding errors
        return "Error: Could not decode the response from the physics database."

tools = [
    Tool(
        name="Physics Q&A Database",
        func=get_physics_answer,
        description="Use this tool when you need to answer questions about specific physics concepts, laws, or formulas. It provides definitive answers from a structured database."
    )
]

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Agent querying API endpoint
@app.post("/ask-agent")
async def ask(req: AgentRequest):
    # Using ainvoke for more structured output and compatibility with newer LangChain versions
    response = await agent.ainvoke({"input": req.question})
    return {"response": response.get("output")}
