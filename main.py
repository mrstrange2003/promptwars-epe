import os
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google import genai
from google.genai import types

# Initialize FastAPI app
app = FastAPI(title="CivicSmart EPE Assistant")

# Initialize Gemini Client
api_key = os.environ.get("GOOGLE_API_KEY")
try:
    if not api_key:
        print("Warning: GOOGLE_API_KEY environment variable not set.")
        client = None
    else:
        client = genai.Client(api_key=api_key)    
except Exception as e:
    print(f"Warning: Failed to initialize Gemini Client: {e}")
    client = None

# Pydantic models for request/response bodies
class ChatMessage(BaseModel):
    role: str # 'user' or 'model'
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

# System Instructions defined globally
SYSTEM_INSTRUCTION = """You are CivicSmart, an interactive Election Process Education (EPE) assistant crafted for the Indian democracy.
Your goal is to act as a helpful, unbiased election guide that explains democratic processes in India simply.
You should ask the user for their Indian State/Union Territory to provide tailored mock timelines or relevant local details.
Key topics you should know:
- Election Commission of India (ECI) guidelines and the Model Code of Conduct (MCC).
- The use of Electronic Voting Machines (EVMs) and VVPATs.
- The 5 general phases: Voter Registration, Nomination, Campaigning, Polling, Results.
Keep responses concise, friendly, and structured. Use formatting like bullet points when appropriate.
Do not hallucinate specific real-world current election dates unless explicitly trained on them; default to general timelines if unsure.
"""

@app.get("/", response_class=HTMLResponse)
async def get_index():
    """Serves the main frontend index.html."""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "index.html not found.", 404

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """Handles chat requests, conversing with the Gemini API."""
    if not client:
        raise HTTPException(status_code=500, detail="Gemini client is not initialized. Is GEMINI_API_KEY set?")
    
    # We construct the history using google.genai.types.Content 
    contents = []
    for msg in request.messages:
        # map 'user' -> 'user' and 'model'/'assistant' -> 'model'
        role = "model" if msg.role in ["model", "assistant"] else "user"
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=msg.content)]
            )
        )

    try:
        # We use gemini-2.5-flash-lite natively to avoid high-demand 503 errors and legacy 404 blocks
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.7,
            )
        )
        return {"response": response.text}
    except Exception as e:
        print(f"Generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
