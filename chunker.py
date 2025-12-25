import os
import json
import re
import cohere
from dotenv import load_dotenv # Add this

load_dotenv() # Add this line at the top of your script

# Initialize the Cohere client
# Make sure to set the COHERE_API_KEY environment variable
co = cohere.Client(os.getenv("COHERE_API_KEY")) 


def chunk_text(text, url, max_tokens=512):
    chunks = []
    
    # Split text into paragraphs
    paragraphs = text.split('\n\n')
    
    current_chunk = ""
    for para in paragraphs:
        # Check if adding the next paragraph would exceed the max token count
        if len(co.tokenize(text=current_chunk + para).tokens) > max_tokens:
            chunks.append({"url": url, "text": current_chunk.strip()})
            current_chunk = ""
            
        current_chunk += para + "\n\n"
        
    # Add the last remaining chunk
    if current_chunk:
        chunks.append({"url": url, "text": current_chunk.strip()})
        
    return chunks

def main():
    with open("crawled_content.txt", "r", encoding="utf-8") as f:
        content = f.read()
        
    # Split the content by URL
    url_contents = re.split(r'URL: ', content)
    
    all_chunks = []
    for url_content in url_contents:
        if not url_content.strip():
            continue
            
        lines = url_content.split('\n')
        url = lines[0]
        text_content = '\n'.join(lines[2:])
        
        chunks = chunk_text(text_content, url)
        all_chunks.extend(chunks)
        
    with open("chunks.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)
        
    print("Chunking finished. Chunks saved to chunks.json")

if __name__ == '__main__':
    main()
