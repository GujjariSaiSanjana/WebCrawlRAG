import os
import sys
from dotenv import load_dotenv

# Add the current directory to sys.path to allow imports from app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.vector_store import get_vector_store

def inspect_db():
    print("--- ChromaDB Inspection Tool ---")
    
    try:
        vector_db = get_vector_store()
        
        # Get all data from the collection
        data = vector_db.get()
        ids = data.get('ids', [])
        metadatas = data.get('metadatas', [])
        documents = data.get('documents', [])
        
        total_records = len(ids)
        print(f"Total records in database: {total_records}")
        
        if total_records == 0:
            print("The database is currently empty.")
            return

        # Group by source
        sources = {}
        for meta in metadatas:
            src = meta.get('source', 'unknown')
            sources[src] = sources.get(src, 0) + 1
            
        print("\nStored Sources:")
        for src, count in sources.items():
            print(f"- {src}: {count} chunks")
            
        print("\nSample Data (First 3 chunks):")
        for i in range(min(3, total_records)):
            print(f"\nID: {ids[i]}")
            print(f"Source: {metadatas[i].get('source')}")
            print(f"Content Snippet: {documents[i][:200]}...")
            print("-" * 30)

    except Exception as e:
        print(f"ERROR: Could not inspect database: {e}")

if __name__ == "__main__":
    load_dotenv()
    inspect_db()
