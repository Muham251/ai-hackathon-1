# import os
# import cohere
# import openai
# import psycopg2
# from fastapi import FastAPI
# from pydantic import BaseModel
# from qdrant_client import QdrantClient

# app = FastAPI()

# # --- 1. SETUP YOUR KEYS ---
# COHERE_KEY = "0KMIXGuLbdexOa2B7alE9IQTw06yki4hyXi1U2J3"
# # Get these from your Neon Dashboard
# NEON_DB_URL = "postgresql://neondb_owner:npg_7uL2wpehVvDG@ep-frosty-star-adyj01ty-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"
# # Use your OpenAI Key here
# OPENAI_KEY = "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" 

# # --- 2. CONNECT TO TOOLS ---
# cohere_client = cohere.Client(COHERE_KEY)
# qdrant = QdrantClient(
#     url="https://1acb0922-00c5-44e3-9e3d-3121efbffeae.us-east4-0.gcp.cloud.qdrant.io:6333", 
#     api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.mPLPzh_zaPwZeUgwwuJJYvvRIPh_sEePuQcwoY1wZlg",
# )
# openai_client = openai.OpenAI(api_key=OPENAI_KEY)

# class ChatRequest(BaseModel):
#     question: str
#     selected_text: str = None  # This handles the "Selected Text" requirement

# # --- 3. THE CHAT LOGIC ---
# @app.post("/chat")
# async def chat_endpoint(req: ChatRequest):
#     # If user selected text, use ONLY that. Otherwise, use Qdrant search.
#     if req.selected_text:
#         context = req.selected_text
#     else:
#         # Search Qdrant for book content
#         emb = cohere_client.embed(texts=[req.question], model="embed-english-v3.0", input_type="search_query").embeddings[0]
#         search_result = qdrant.search(collection_name="humanoid_ai_book", query_vector=emb, limit=3)
#         context = "\n".join([res.payload['text'] for res in search_result])

#     # Ask OpenAI to answer based on the book content
#     response = openai_client.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "system", "content": f"You are an AI book assistant. Answer using this content: {context}"},
#             {"role": "user", "content": req.question}
#         ]
#     )
#     answer = response.choices[0].message.content

#     # SAVE TO NEON DATABASE
#     conn = psycopg2.connect(NEON_DB_URL)
#     with conn.cursor() as cur:
#         cur.execute("INSERT INTO chat_history (question, answer) VALUES (%s, %s)", (req.question, answer))
#         conn.commit()
#     conn.close()

#     return {"answer": answer}




















































# import os
# import cohere
# import psycopg2
# from fastapi import FastAPI
# from pydantic import BaseModel
# from qdrant_client import QdrantClient
# from openai import OpenAI  # Groq uses the OpenAI library format

# app = FastAPI()

# # --- 1. SETUP YOUR FREE/EXISTING KEYS ---
# COHERE_KEY = "0KMIXGuLbdexOa2B7alE9IQTw06yki4hyXi1U2J3"
# NEON_DB_URL = "postgresql://neondb_owner:npg_7uL2wpehVvDG@ep-frosty-star-adyj01ty-pooler.c-2.us-east-1.aws.neon.tech/neondb"
# # PASTE YOUR NEW GROQ KEY HERE
# GROQ_API_KEY = "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" 

# # --- 2. CONNECT TO TOOLS ---
# cohere_client = cohere.Client(COHERE_KEY)
# qdrant = QdrantClient(
#     url="https://1acb0922-00c5-44e3-9e3d-3121efbffeae.us-east4-0.gcp.cloud.qdrant.io:6333", 
#     api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.mPLPzh_zaPwZeUgwwuJJYvvRIPh_sEePuQcwoY1wZlg",
# )

# # This connects to Groq using the OpenAI-compatible format
# groq_client = OpenAI(
#     base_url="https://api.groq.com/openai/v1",
#     api_key=GROQ_API_KEY
# )

# class ChatRequest(BaseModel):
#     question: str
#     selected_text: str = None

# # --- 3. THE CHAT LOGIC ---
# @app.post("/chat")
# async def chat_endpoint(req: ChatRequest):
#     try:
#         print("--- Step 1: Getting context ---")
#         if req.selected_text and req.selected_text.strip():
#             context = req.selected_text
#         else:
#             emb = cohere_client.embed(texts=[req.question], model="embed-english-v3.0", input_type="search_query").embeddings[0]
#             search_result = qdrant.search(collection_name="humanoid_ai_book", query_vector=emb, limit=3)
#             context = "\n".join([res.payload['text'] for res in search_result])

#         print("--- Step 2: Calling Groq (Free AI) ---")
#         response = groq_client.chat.completions.create(
#             model="llama-3.3-70b-versatile", # High-quality free model
#             messages=[
#                 {"role": "system", "content": f"You are an AI book assistant. Answer using this content: {context}"},
#                 {"role": "user", "content": req.question}
#             ]
#         )
#         answer = response.choices[0].message.content

#         print("--- Step 3: Connecting to Neon ---")
#         conn = psycopg2.connect(NEON_DB_URL)
        
#         print("--- Step 4: Saving to Database ---")
#         with conn.cursor() as cur:
#             cur.execute("INSERT INTO chat_history (question, answer) VALUES (%s, %s)", (req.question, answer))
#             conn.commit()
#         conn.close()

#         print("--- Step 5: Done! ---")
#         return {"answer": answer}

#     except Exception as e:
#         print(f"!!! ERROR DETECTED: {str(e)}")
#         return {"error": str(e)}


















# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# class ChatRequest(BaseModel):
#     question: str
#     selected_text: str = None

# @app.post("/chat")
# async def chat_endpoint(req: ChatRequest):
#     print(f"--- I RECEIVED YOUR QUESTION: {req.question} ---")
#     return {
#         "answer": "SUCCESS! Your server is working perfectly. The problem was likely a slow connection to the database or AI."
#     }

# @app.get("/")
# async def root():
#     return {"message": "Server is running!"}






























# import os
# import cohere
# from fastapi import FastAPI
# from pydantic import BaseModel
# from qdrant_client import QdrantClient
# from openai import OpenAI

# app = FastAPI()

# # --- KEYS ---
# COHERE_KEY = "0KMIXGuLbdexOa2B7alE9IQTw06yki4hyXi1U2J3"
# GROQ_API_KEY = "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" 

# cohere_client = cohere.Client(COHERE_KEY)
# qdrant = QdrantClient(
#     url="https://1acb0922-00c5-44e3-9e3d-3121efbffeae.us-east4-0.gcp.cloud.qdrant.io:6333", 
#     api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.mPLPzh_zaPwZeUgwwuJJYvvRIPh_sEePuQcwoY1wZlg",
# )
# groq_client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=GROQ_API_KEY)

# class ChatRequest(BaseModel):
#     question: str
#     selected_text: str = None

# @app.post("/chat")
# async def chat_endpoint(req: ChatRequest):
#     try:
#         # 1. Get Context
#         print("--- Step 1: Getting context ---")
#         if req.selected_text and req.selected_text.strip():
#             context = req.selected_text
#         else:
#             emb = cohere_client.embed(texts=[req.question], model="embed-english-v3.0", input_type="search_query").embeddings[0]
#             search_result = qdrant.search(collection_name="humanoid_ai_book", query_vector=emb, limit=3)
#             context = "\n".join([res.payload['text'] for res in search_result])

#         # 2. Get AI Answer from Groq
#         print("--- Step 2: Calling Groq ---")
#         response = groq_client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[
#                 {"role": "system", "content": f"You are an AI assistant. Use this: {context}"},
#                 {"role": "user", "content": req.question}
#             ]
#         )
#         answer = response.choices[0].message.content

#         # 3. DATABASE (DISABLED FOR THIS TEST)
#         print("--- Step 3: Skipping Database for speed ---")
        
#         print("--- Step 4: Done! ---")
#         return {"answer": answer}

#     except Exception as e:
#         print(f"!!! ERROR: {str(e)}")
#         return {"error": str(e)}
































# import os
# import cohere
# from fastapi import FastAPI
# from pydantic import BaseModel
# from qdrant_client import QdrantClient
# from openai import OpenAI

# app = FastAPI()

# # --- KEYS ---
# COHERE_KEY = "0KMIXGuLbdexOa2B7alE9IQTw06yki4hyXi1U2J3"
# GROQ_API_KEY = "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" 

# cohere_client = cohere.Client(COHERE_KEY)
# qdrant = QdrantClient(
#     url="https://1acb0922-00c5-44e3-9e3d-3121efbffeae.us-east4-0.gcp.cloud.qdrant.io:6333", 
#     api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.mPLPzh_zaPwZeUgwwuJJYvvRIPh_sEePuQcwoY1wZlg",
# )
# groq_client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=GROQ_API_KEY)

# class ChatRequest(BaseModel):
#     question: str
#     selected_text: str = None

# @app.post("/chat")
# async def chat_endpoint(req: ChatRequest):
#     try:
#         # 1. Get Context
#         print("--- Step 1: Getting context ---")
#         if req.selected_text and req.selected_text.strip():
#             context = req.selected_text
#         else:
#             # Generate embedding for the search query
#             emb = cohere_client.embed(
#                 texts=[req.question], 
#                 model="embed-english-v3.0", 
#                 input_type="search_query"
#             ).embeddings[0]
            
#             # --- THE FIX IS HERE ---
#             # Changed qdrant.search to qdrant.query_points
#             search_result = qdrant.query_points(
#                 collection_name="humanoid_ai_book", 
#                 query=emb, 
#                 limit=3
#             ).points
            
#             context = "\n".join([res.payload['text'] for res in search_result])

#         # 2. Get AI Answer from Groq
#         print("--- Step 2: Calling Groq ---")
#         response = groq_client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[
#                 {"role": "system", "content": f"You are an AI assistant. Use this: {context}"},
#                 {"role": "user", "content": req.question}
#             ]
#         )
#         answer = response.choices[0].message.content

#         # 3. DATABASE (DISABLED FOR THIS TEST)
#         print("--- Step 3: Skipping Database for speed ---")
        
#         print("--- Step 4: Done! ---")
#         return {"answer": answer}

#     except Exception as e:
#         print(f"!!! ERROR: {str(e)}")
#         return {"error": str(e)}









import os
import cohere
import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel
from qdrant_client import QdrantClient
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- KEYS (Now loading from Environment Variables) ---
# DO NOT paste the actual keys here. 
# You will add them to the Vercel/System environment variables instead.
COHERE_KEY = os.getenv("COHERE_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY") 
NEON_DB_URL = os.getenv("NEON_DB_URL")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

cohere_client = cohere.Client(COHERE_KEY)
qdrant = QdrantClient(
    url=QDRANT_URL, 
    api_key=QDRANT_API_KEY,
)
# The correct way to use Groq with the OpenAI library:
groq_client = OpenAI(
    base_url="https://api.groq.com/openai/v1", 
    api_key=os.getenv("GROQ_API_KEY")
)
class ChatRequest(BaseModel):
    question: str
    selected_text: str = None

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        # 1. Get Context (RAG)
        if req.selected_text and req.selected_text.strip():
            context = req.selected_text
        else:
            emb = cohere_client.embed(
                texts=[req.question], 
                model="embed-english-v3.0", 
                input_type="search_query"
            ).embeddings[0]
            
            search_result = qdrant.query_points(
                collection_name="humanoid_ai_book", 
                query=emb, 
                limit=3
            ).points
            context = "\n".join([res.payload['text'] for res in search_result])

        # 2. Get AI Answer
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"You are an AI assistant. Use this: {context}"},
                {"role": "user", "content": req.question}
            ]
        )
        answer = response.choices[0].message.content

        # 3. SAVE TO NEON DATABASE
        conn = psycopg2.connect(NEON_DB_URL)
        with conn.cursor() as cur:
            cur.execute("INSERT INTO chat_history (question, answer) VALUES (%s, %s)", (req.question, answer))
            conn.commit()
        conn.close()

        return {"answer": answer}

    except Exception as e:
        return {"error": str(e)}