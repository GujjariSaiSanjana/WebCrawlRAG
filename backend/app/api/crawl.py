from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.services.crawler import crawl_url
from app.services.chunker import chunk_text
from app.services.vector_store import get_vector_store

router = APIRouter()

class CrawlRequest(BaseModel):
    urls: List[str]
    clear: bool = False

@router.post("/crawl")
def crawl_and_store(request: CrawlRequest):
    print(f"DEBUG: Starting crawl for URLs: {request.urls} (clear={request.clear})")
    vector_db = get_vector_store()
    
    if request.clear:
        print("DEBUG: Clearing existing vector store...")
        try:
            # Chroma implementation to delete all
            ids = vector_db.get()['ids']
            if ids:
                vector_db.delete(ids)
                print(f"DEBUG: Deleted {len(ids)} existing records")
        except Exception as e:
            print(f"WARNING: Could not clear vector store: {e}")

    stored_chunks = 0

    for url in request.urls:
        print(f"DEBUG: Crawling {url}...")
        data = crawl_url(url)
        
        # Debug: Show what we got back
        if "error" in data:
            print(f"ERROR: Failed to crawl {url}: {data['error']}")
            continue
        
        if "content" in data:
            content_length = len(data["content"])
            print(f"DEBUG: Extracted {content_length} characters from {url}")
            
            if content_length == 0:
                print(f"WARNING: No content extracted from {url}")
                continue
            
            chunks = chunk_text(data["content"])
            print(f"DEBUG: Split into {len(chunks)} chunks")
            print(f"DEBUG: Storing {len(chunks)} chunks...")
            vector_db.add_texts(
                texts=chunks,
                metadatas=[{"source": url}] * len(chunks)
            )
            stored_chunks += len(chunks)
        else:
            print(f"WARNING: No 'content' key in response for {url}")

    print(f"DEBUG: Finished crawl. Total chunks stored: {stored_chunks}")
    return {"status": "stored", "chunks": stored_chunks}
