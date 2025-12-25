import os
import subprocess
import json
from dotenv import load_dotenv # Add this

load_dotenv() # Add this line at the top of your script



def run_script(script_name, *args):
    """Helper function to run Python scripts."""
    command = ["python", script_name] + list(args)
    print(f"\nRunning: {' '.join(command)}")
    process = subprocess.run(command, capture_output=True, text=True, check=True)
    print(process.stdout)
    if process.stderr:
        print(f"Stderr: {process.stderr}")

def main(start_url, collection_name="docusaurus_book"):
    # Step 1: Crawl the website
    # The crawler.py script saves content to 'crawled_content.txt'
    run_script("crawler.py", start_url)
    
    # Step 2: Chunk the content
    # The chunker.py script reads 'crawled_content.txt' and saves chunks to 'chunks.json'
    run_script("chunker.py")
    
    # Step 3: Generate embeddings
    # The embedder.py script reads 'chunks.json' and saves embeddings to 'embedded_chunks.json'
    run_script("embedder.py")
    
    # Step 4: Upload to Qdrant
    # The qdrant_uploader.py script reads 'embedded_chunks.json' and uploads to Qdrant
    run_script("qdrant_uploader.py", collection_name)
    
    print("\nWebsite ingestion and embedding pipeline completed successfully!")

if __name__ == '__main__':
    # Ensure COHERE_API_KEY is set in your environment
    if "COHERE_API_KEY" not in os.environ:
        print("Error: COHERE_API_KEY environment variable not set.")
        exit(1)
        
    # The deployed Docusaurus URL
    docusaurus_url = "https://Muham251.github.io/ai-hackathon-1/"
    
    # You can customize the Qdrant collection name
    qdrant_collection = "docusaurus_book"
    
    main(docusaurus_url, qdrant_collection)
