from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.services.crawler import crawl_url
from app.services.chunker import chunk_text
from app.services.vector_store import get_vector_store

router = APIRouter()

class CrawlRequest(BaseModel):
    urls: List[str]

@router.post("/crawl")
def crawl_and_store(request: CrawlRequest):
    vector_db = get_vector_store()
    stored_chunks = 0

    for url in request.urls:
        data = crawl_url(url)

        if "content" in data:
            chunks = chunk_text(data["content"])
            vector_db.add_texts(
                texts=chunks,
                metadatas=[{"source": url}] * len(chunks)
            )
            stored_chunks += len(chunks)

    vector_db.persist()
    return {"status": "stored", "chunks": stored_chunks}
