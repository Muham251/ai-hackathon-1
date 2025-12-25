import os
import requests
import xml.etree.ElementTree as ET
import trafilatura
import cohere
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

SITEMAP_URL = "https://ai-hackathon-1.vercel.app/sitemap.xml"
REAL_DOMAIN = "https://ai-hackathon-1.vercel.app"
COLLECTION_NAME = "humanoid_ai_book"

cohere_client = cohere.Client("0KMIXGuLbdexOa2B7alE9IQTw06yki4hyXi1U2J3")
EMBED_MODEL = "embed-english-v3.0"

qdrant = QdrantClient(
    url="https://1acb0922-00c5-44e3-9e3d-3121efbffeae.us-east4-0.gcp.cloud.qdrant.io:6333",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.mPLPzh_zaPwZeUgwwuJJYvvRIPh_sEePuQcwoY1wZlg",
)

def get_all_urls(sitemap_url):
    xml = requests.get(sitemap_url).text
    root = ET.fromstring(xml)

    urls = []
    for child in root:
        loc_tag = child.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        if loc_tag is not None:
            raw_url = loc_tag.text
            clean_url = raw_url.replace(
                "https://your-docusaurus-site.example.com",
                REAL_DOMAIN
            )
            urls.append(clean_url)

    print("\nFOUND URLS:")
    for u in urls:
        print(" -", u)

    return urls

def extract_text_from_url(url):
    try:
        html = requests.get(url, timeout=10).text
        text = trafilatura.extract(html)
        return text
    except Exception as e:
        print(f"[ERROR] Could not download {url}: {e}")
        return None

def chunk_text(text, max_chars=1200):
    chunks = []
    if not text:
        return chunks

    while len(text) > max_chars:
        split_pos = text[:max_chars].rfind(". ")
        if split_pos == -1:
            split_pos = max_chars
        chunks.append(text[:split_pos])
        text = text[split_pos:]

    chunks.append(text)
    return chunks

def embed(text):
    response = cohere_client.embed(
        model=EMBED_MODEL,
        input_type="search_query",
        texts=[text],
    )
    return response.embeddings[0]

def create_collection():
    print("\nCreating Qdrant collection...")

    if qdrant.collection_exists(COLLECTION_NAME):
        qdrant.delete_collection(COLLECTION_NAME)

    qdrant.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=1024,
            distance=Distance.COSINE
        )
    )

def save_chunk_to_qdrant(chunk, chunk_id, url):
    vector = embed(chunk)
    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=chunk_id,
                vector=vector,
                payload={
                    "url": url,
                    "text": chunk,
                    "chunk_id": chunk_id
                }
            )
        ]
    )

def ingest_book():
    urls = get_all_urls(SITEMAP_URL)
    create_collection()
    global_id = 1

    for url in urls:
        print("\nProcessing:", url)
        text = extract_text_from_url(url)
        if not text:
            continue

        chunks = chunk_text(text)
        for ch in chunks:
            save_chunk_to_qdrant(ch, global_id, url)
            print(f"Saved chunk {global_id}")
            global_id += 1

    print("\n✔️ Ingestion completed!")

if __name__ == "__main__":
    ingest_book()
