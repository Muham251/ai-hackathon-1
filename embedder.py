import json
import cohere
import os
from dotenv import load_dotenv # Add this

load_dotenv() # Add this line at the top of your script
# Initialize Cohere client
co = cohere.Client(os.environ.get("COHERE_API_KEY"))

def generate_embeddings(chunks_file, embeddings_output_file):
    with open(chunks_file, 'r', encoding='utf-8') as f:
        chunks = json.load(f)

    texts_to_embed = [chunk['text'] for chunk in chunks]
    
    # Cohere has a limit of 96 texts per request
    # Embed in batches
    embedded_chunks = []
    batch_size = 96
    for i in range(0, len(texts_to_embed), batch_size):
        batch_texts = texts_to_embed[i:i + batch_size]
        try:
            response = co.embed(
                texts=batch_texts,
                model='embed-english-v3.0', # Using a general purpose embedding model
                input_type='search_document'
            ).embeddings
            
            for j, embedding in enumerate(response):
                chunks[i + j]['embedding'] = embedding
                embedded_chunks.append(chunks[i+j])

        except cohere.CohereAPIError as e:
            print(f"Cohere API error: {e}")
            print(f"Error occurred in batch starting at index {i}. Skipping this batch.")
            # Depending on error type, you might want to retry or handle specifically
            continue
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print(f"Error occurred in batch starting at index {i}. Skipping this batch.")
            continue

    with open(embeddings_output_file, 'w', encoding='utf-8') as f:
        json.dump(embedded_chunks, f, indent=2)
    
    print(f"Embeddings generated and saved to {embeddings_output_file}")

if __name__ == '__main__':
    generate_embeddings('chunks.json', 'embedded_chunks.json')
