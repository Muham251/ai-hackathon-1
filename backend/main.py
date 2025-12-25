import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import trafilatura
import cohere
from qdrant_client import QdrantClient, models
import json

# Initialize clients
co = cohere.Client(os.environ.get("COHERE_API_KEY"))
qdrant_client = QdrantClient(":memory:")

def get_all_urls(start_url):
    """Recursively crawls a website to get all unique URLs."""
    visited = set()
    to_visit = {start_url}
    
    while to_visit:
        url = to_visit.pop()
        if url in visited:
            continue
            
        print(f"Crawling: {url}")
        visited.add(url)
        
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                joined_url = urljoin(url, href)
                
                if urlparse(joined_url).netloc == urlparse(start_url).netloc:
                    to_visit.add(joined_url)
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch {url}: {e}")
            
    return list(visited)

def extract_text_from_url(url):
    """Extracts the main text content from a URL."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return trafilatura.extract(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Failed to extract text from {url}: {e}")
        return None

def chunk_text(text, max_tokens=512):
    """Chunks text into smaller pieces based on token count."""
    if not text:
        return []
    
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        if len(co.tokenize(text=current_chunk + para, model='embed-english-v3.0').tokens) > max_tokens:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = para
        else:
            current_chunk += "\n\n" + para
            
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks

def embed(chunks, model='embed-english-v3.0', input_type='search_document'):
    """Generates embeddings for a list of text chunks."""
    embeddings = []
    batch_size = 96
    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i:i+batch_size]
        response = co.embed(texts=batch_chunks, model=model, input_type=input_type)
        embeddings.extend(response.embeddings)
    return embeddings

def create_collection(collection_name="rag_embedding", vector_size=1024):
    """Creates a Qdrant collection."""
    try:
        qdrant_client.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
        )
        print(f"Collection '{collection_name}' created successfully.")
    except Exception as e:
        print(f"Could not create collection: {e}")

def save_chunk_to_qdrant(collection_name, chunks, embeddings):
    """Saves chunks and their embeddings to Qdrant."""
    points = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        points.append(
            models.PointStruct(
                id=i,
                vector=embedding,
                payload={"text": chunk}
            )
        )
        
    qdrant_client.upsert(
        collection_name=collection_name,
        wait=True,
        points=points
    )
    print(f"Successfully uploaded {len(points)} points to Qdrant collection '{collection_name}'.")


def main():
    """Main function to run the ingestion pipeline."""
    if "COHERE_API_KEY" not in os.environ:
        print("Error: COHERE_API_KEY environment variable not set.")
        return
        
    start_url = "https://ai-hackathon-1.vercel.app/"
    collection_name = "rag_embedding"
    
    # 1. Get all URLs
    all_urls = get_all_urls(start_url)
    
    all_chunks = []
    for url in all_urls:
        # 2. Extract text from each URL
        text = extract_text_from_url(url)
        if text:
            # 3. Chunk the text
            chunks = chunk_text(text)
            all_chunks.extend(chunks)
            
    if all_chunks:
        # 4. Generate embeddings
        embeddings = embed(all_chunks)
        
        # 5. Create Qdrant collection
        vector_size = len(embeddings[0])
        create_collection(collection_name, vector_size)
        
        # 6. Save chunks to Qdrant
        save_chunk_to_qdrant(collection_name, all_chunks, embeddings)
        
    print("\nPipeline finished.")

if __name__ == "__main__":
    main()
