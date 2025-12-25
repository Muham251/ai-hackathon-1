import cohere
from qdrant_client import QdrantClient

# Initialize Cohere client
# This acts as the "Brain" to turn text into numbers
cohere_client = cohere.Client("0KMIXGuLbdexOa2B7alE9IQTw06yki4hyXi1U2J3") 

# Connect to Qdrant
# This acts as the "Memory" to store your module data
qdrant = QdrantClient(
     url="https://1acb0922-00c5-44e3-9e3d-3121efbffeae.us-east4-0.gcp.cloud.qdrant.io:6333", 
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.mPLPzh_zaPwZeUgwwuJJYvvRIPh_sEePuQcwoY1wZlg",

)

def get_embedding(text):
    """Turns your book text into a vector (list of numbers)."""
    response = cohere_client.embed(
        texts=[text],
        model="embed-english-v3.0",
        input_type="search_query",
    )
    return response.embeddings[0]

def retrieve(query):
    embedding = get_embedding(query)
    result = qdrant.query_points(
        collection_name="humanoid_ai_book", # Make sure this matches your collection name
        query=embedding,
        limit=5
    )
    return [point.payload["text"] for point in result.points]
print(retrieve("What data do you have"))