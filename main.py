import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import psycopg2
from agent import agent  # IMPORT YOUR NEW AGENT HERE

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

def save_to_neon(question, answer):
    try:
        conn = psycopg2.connect(os.getenv("NEON_DATABASE_URL"))
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id SERIAL PRIMARY KEY,
                question TEXT,
                answer TEXT
            );
        """)
        cur.execute(
            "INSERT INTO chat_history (question, answer) VALUES (%s, %s)",
            (question, answer)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database Error: {e}")

class ChatRequest(BaseModel):
    question: str
    selected_text: str = None

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

@app.post("/chat")
async def chat(request: ChatRequest):
    # Using Pydantic AI Agent
    # If the user selected text, we pass it as context. 
    # Otherwise, the agent uses its 'retrieve' tool automatically.
    prompt = request.question
    if request.selected_text:
        prompt = f"Context: {request.selected_text}\n\nQuestion: {request.question}"

    try:
        # Run the agent (Pydantic AI handles tools like Qdrant/Cohere automatically)
        result = await agent.run(prompt)
        answer = result.data
        
        # Save to database
        save_to_neon(request.question, answer)
        
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"Agent Error: {str(e)}"}


