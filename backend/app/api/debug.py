from fastapi import APIRouter
from app.services.vector_store import get_vector_store

router = APIRouter()

@router.get("/db/stats")
def get_db_stats():
    """Get statistics about the vector database."""
    try:
        vector_db = get_vector_store()
        
        # Get all data from ChromaDB
        data = vector_db.get()
        
        total_chunks = len(data['ids'])
        
        # Count chunks per source
        sources = {}
        for metadata in data['metadatas']:
            source = metadata.get('source', 'unknown')
            sources[source] = sources.get(source, 0) + 1
        
        return {
            "total_chunks": total_chunks,
            "sources": sources,
            "sample_ids": data['ids'][:5] if data['ids'] else []
        }
    except Exception as e:
        return {"error": str(e)}

@router.get("/db/view")
def view_db_content():
    """View actual content stored in the database."""
    try:
        vector_db = get_vector_store()
        data = vector_db.get()
        
        # Return first 3 chunks with their content
        samples = []
        for i in range(min(3, len(data['ids']))):
            samples.append({
                "id": data['ids'][i],
                "source": data['metadatas'][i].get('source', 'unknown'),
                "content_preview": data['documents'][i][:200] + "..." if len(data['documents'][i]) > 200 else data['documents'][i]
            })
        
        return {
            "total_chunks": len(data['ids']),
            "samples": samples
        }
    except Exception as e:
        return {"error": str(e)}

@router.post("/db/clear")
def clear_database():
    """Clear all data from the vector database."""
    try:
        vector_db = get_vector_store()
        data = vector_db.get()
        
        if data['ids']:
            vector_db.delete(data['ids'])
            return {"status": "cleared", "deleted_count": len(data['ids'])}
        else:
            return {"status": "already_empty", "deleted_count": 0}
    except Exception as e:
        return {"error": str(e)}
