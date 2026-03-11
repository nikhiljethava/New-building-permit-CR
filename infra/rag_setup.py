import os
import time
from google.cloud import aiplatform
from vertexai.preview import rag
import vertexai

# Configuration
PROJECT_ID = os.popen("gcloud config get-value project").read().strip()
LOCATION = "us-west1"
CORPUS_DISPLAY_NAME = "ca-building-codes"
BUILDING_CODES_DIR = "../building-codes"

def setup_rag():
    print(f"Initializing Vertex AI for project {PROJECT_ID} in {LOCATION}...")
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    # 1. Create Corpus if it doesn't exist
    print(f"Checking for existing corpus: {CORPUS_DISPLAY_NAME}...")
    existing_corpora = rag.list_rag_corpora()
    corpus = None
    for c in existing_corpora:
        if c.display_name == CORPUS_DISPLAY_NAME:
            corpus = c
            print(f"Found existing corpus: {corpus.name}")
            break

    if not corpus:
        print(f"Creating RAG Corpus: {CORPUS_DISPLAY_NAME}...")
        corpus = rag.create_rag_corpus(
            display_name=CORPUS_DISPLAY_NAME,
            # Initializing with default embedding model
        )
        print(f"Created corpus: {corpus.name}")

    # 2. Upload files
    print(f"Uploading files from {BUILDING_CODES_DIR}...")
    files = [f for f in os.listdir(BUILDING_CODES_DIR) if f.endswith(".pdf")]
    
    for filename in files:
        file_path = os.path.join(BUILDING_CODES_DIR, filename)
        print(f"Uploading {filename}...")
        try:
            rag.import_files(
                corpus_name=corpus.name,
                paths=[file_path],
                chunk_size=1024,
                chunk_overlap=200,
            )
            print(f"Successfully started import for {filename}")
        except Exception as e:
            print(f"Failed to upload {filename}: {e}")

    print("RAG setup script completed.")

if __name__ == "__main__":
    setup_rag()
