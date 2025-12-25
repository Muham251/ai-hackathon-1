import json
import os
from qdrant_client import QdrantClient, models

def upload_to_qdrant(embedded_chunks_file, collection_name="docusaurus_book"):
    # Initialize Qdrant client
    # For a local in-memory instance:
    client = QdrantClient(":memory:") 

    # If you have a remote Qdrant instance, uncomment and configure these lines:
    # QDRANT_HOST = os.environ.get("QDRANT_HOST")
    # QDRANT_PORT = os.environ.get("QDRANT_PORT")
    # QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")
    # client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY)


    # Load embedded chunks
    with open(embedded_chunks_file, 'r', encoding='utf-8') as f:
        embedded_chunks = json.load(f)

    # Get the vector size from the first embedding
    vector_size = len(embedded_chunks[0]['embedding'])

    # Create collection if it doesn't exist
    try:
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
        )
        print(f"Collection '{collection_name}' recreated.")
    except Exception as e:
        print(f"Error recreating collection: {e}. Attempting to use existing collection.")
        # If recreate fails (e.g., collection already exists and client.recreate_collection doesn't support
        # checking existence easily, or other issues), try to get info to ensure it exists.
        # This part might need refinement based on actual Qdrant client behavior for existence checks.
        try:
            client.get_collection(collection_name=collection_name)
            print(f"Collection '{collection_name}' already exists.")
        except Exception as e_get:
            print(f"Collection '{collection_name}' does not exist and could not be created: {e_get}")
            return

    # Prepare points for upsertion
    points = []
    for i, chunk in enumerate(embedded_chunks):
        points.append(
            models.PointStruct(
                id=i,
                vector=chunk['embedding'],
                payload={"url": chunk['url'], "text": chunk['text']}
            )
        )

    # Upload points to Qdrant
    client.upsert(
        collection_name=collection_name,
        wait=True,
        points=points
    )
    print(f"Successfully uploaded {len(points)} points to Qdrant collection '{collection_name}'.")

if __name__ == '__main__':
    upload_to_qdrant('embedded_chunks.json')
