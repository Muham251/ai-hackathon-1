# import os
# import asyncio
# import cohere
# from openai import AsyncOpenAI
# from dotenv import load_dotenv
# from qdrant_client import QdrantClient
# from pydantic_ai import Agent, RunContext
# from pydantic_ai.models.openai import OpenAIChatCompletionsModel
# # ... other imports like cohere and qdrant
# # 1. SETUP
# load_dotenv()

# # Setup Provider (Groq)
# # Use GROQ_API_KEY as defined in your .env file
# provider = AsyncOpenAI(
#     api_key=os.getenv("GROQ_API_KEY"), 
#     base_url="https://api.groq.com/openai/v1"
# )

# model = OpenAIChatCompletionsModel(
#     model="llama-3.3-70b-versatile", 
#     openai_client=provider
# )

# # 2. VECTOR DB TOOLS
# cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))
# qdrant = QdrantClient(
#     url=os.getenv("QDRANT_URL"),
#     api_key=os.getenv("QDRANT_API_KEY")
# )

# # 3. DEFINE THE AGENT
# agent = Agent(
#     model=model,
#     system_prompt=(
#         "You are a helpful Humanoid Robotics Expert tutor. "
#         "Use the 'retrieve' tool to find information in the textbook. "
#         "Answer immediately once you find the data."
#     )
# )

# # 4. TOOLS
# @agent.tool
# async def retrieve(ctx: RunContext, query: str) -> str:
#     """Searches the Physical AI & Robotics textbook for relevant information."""
#     print(f"🔎 Searching textbook for: {query}")
#     try:
#         response = cohere_client.embed(
#             model="embed-english-v3.0",
#             input_type="search_query",
#             texts=[query],
#         )
#         vector = response.embeddings[0]
        
#         # Search the Qdrant collection
#         result = qdrant.query_points(
#             collection_name="humanoid_ai_book",
#             query=vector,
#             limit=3
#         )
#         return "\n---\n".join([point.payload["text"] for point in result.points])
#     except Exception as e:
#         return f"Retrieval Error: {str(e)}"

# # 5. EXECUTION
# if __name__ == "__main__":
#     async def main():
#         # run_sync is used for synchronous execution in pydantic-ai
#         result = await agent.run(
#             "What are the hardware requirements for NVIDIA Isaac Sim?"
#         )
#         print(f"\n--- FINAL ANSWER ---\n{result.data}")

#     asyncio.run(main())


# import os
# import asyncio
# import cohere
# from openai import AsyncOpenAI
# from dotenv import load_dotenv
# from qdrant_client import QdrantClient
# from pydantic_ai import Agent, RunContext
# from pydantic_ai.models.openai import OpenAIChatCompletionsModel

# # 1. SETUP & CLIENTS
# load_dotenv()

# # Initialize external clients
# cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))
# qdrant = QdrantClient(
#     url=os.getenv("QDRANT_URL"), 
#     api_key=os.getenv("QDRANT_API_KEY")
# )

# # Setup LLM Provider (Groq)
# provider = AsyncOpenAI(
#     api_key=os.getenv("GROQ_API_KEY"), 
#     base_url="https://api.groq.com/openai/v1"
# )

# model = OpenAIChatCompletionsModel(
#     model="llama-3.3-70b-versatile", 
#     openai_client=provider
# )

# # 2. DEFINE THE AGENT
# agent = Agent(
#     model=model,
#     system_prompt=(
#         "You are a helpful Humanoid Robotics Expert tutor. "
#         "Use the 'retrieve' tool to look up technical details from the textbook "
#         "before answering complex questions about ROS 2, URDF, or humanoid control."
#     )
# )

# # 3. RETRIEVAL TOOL
# # 3. RETRIEVAL TOOL

# @agent.tool
# async def retrieve(ctx: RunContext, query: str) -> str:
#     """Searches the Physical AI & Robotics textbook for relevant information."""
#     print(f"🔎 Agent is searching textbook for: {query}")
#     try:
#         # 1. Create embedding for the search query
#         # Use the cohere_client you initialized at the top
#         emb_response = cohere_client.embed(
#             model="embed-english-v3.0",
#             input_type="search_query",
#             texts=[query]
#         )
#         query_vector = emb_response.embeddings[0]

#         # 2. Search Qdrant collection
#         search_results = qdrant.query_points(
#             collection_name="humanoid_ai_book",
#             query=query_vector,
#             limit=3
#         ).points

#         # 3. Format results for the LLM
#         context = "\n---\n".join([r.payload["text"] for r in search_results])
#         return context if context else "No relevant information found in the textbook."

#     except Exception as e:
#         # This prevents the IndentationError by providing code to run
#         return f"Retrieval Error: {str(e)}"

# from pydantic_ai.models.openai import OpenAIChatModel
# from pydantic_ai.providers.openai import OpenAIProvider
# import os
# import asyncio
# import cohere
# from openai import AsyncOpenAI
# from dotenv import load_dotenv
# from qdrant_client import QdrantClient
# from pydantic_ai import Agent, RunContext

# # 1. UPDATED IMPORTS
# from pydantic_ai.models.openai import OpenAIChatModel
# from pydantic_ai.providers.openai import OpenAIProvider
# from pydantic_ai import Agent, ModelSettings

# load_dotenv()

# # Setup Clients
# cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))
# qdrant = QdrantClient(
#     url=os.getenv("QDRANT_URL"), 
#     api_key=os.getenv("QDRANT_API_KEY")
# )

# # 2. UPDATED MODEL SETUP (Groq via OpenAI-compatible provider)
# # We define a custom provider for Groq since it uses the OpenAI API standard
# groq_provider = OpenAIProvider(
#     base_url="https://api.groq.com/openai/v1",
#     api_key=os.getenv("GROQ_API_KEY")
# )

# model = OpenAIChatModel(
#     model_name="llama-3.3-70b-versatile",
#     provider=groq_provider,
# )

# # Define your model settings to be more flexible
# settings = ModelSettings(
#     max_tokens=1000,
#     temperature=0.7,
# )


# # 3. REST OF THE AGENT (Same as before)
# agent = Agent(
#     model=model,
#     defer_model_check=True, 
#     model_settings=settings, # Pass settings here
#     system_prompt=(
#         "You are a helpful Humanoid Robotics Expert tutor. "
#         "Use the 'retrieve' tool to search the textbook for information."
#     )
# )




        


import os
import asyncio
import cohere
from openai import AsyncOpenAI
from dotenv import load_dotenv
from qdrant_client import QdrantClient

# CORRECT IMPORTS
from pydantic_ai import Agent, RunContext, ModelSettings
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

load_dotenv()

# 1. SETUP CLIENTS
cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))
qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"), 
    api_key=os.getenv("QDRANT_API_KEY")
)

# 2. CONFIGURE GROQ PROVIDER
groq_provider = OpenAIProvider(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

model = OpenAIChatModel(
    model_name="llama-3.3-70b-versatile",
    provider=groq_provider
)

# 3. DEFINE THE AGENT
agent = Agent(
    model=model,
    # This bypasses the 'service_tier' validation error from Groq
    defer_model_check=True,
    model_settings=ModelSettings(temperature=0.7),
    system_prompt=(
        "You are a helpful Humanoid Robotics Expert tutor. "
        "Use the 'retrieve' tool to search the textbook for information "
        "on URDF, ROS 2, and physical robot simulation."
    )
)

# 4. RETRIEVAL TOOL
@agent.tool
async def retrieve(ctx: RunContext, query: str) -> str:
    """Searches the Physical AI & Robotics textbook for relevant information."""
    print(f"🔎 Agent is searching textbook for: {query}")
    try:
        emb_response = cohere_client.embed(
            model="embed-english-v3.0",
            input_type="search_query",
            texts=[query]
        )
        query_vector = emb_response.embeddings[0]

        search_results = qdrant.query_points(
            collection_name="humanoid_ai_book",
            query=query_vector,
            limit=3
        ).points

        context = "\n---\n".join([r.payload["text"] for r in search_results])
        return context if context else "No relevant information found in the textbook."
    except Exception as e:
        return f"Retrieval Error: {str(e)}"