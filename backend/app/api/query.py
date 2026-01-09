from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rag_chain import run_rag_query

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
def ask_question(request: QueryRequest):
    print(f"DEBUG: Received question: {request.question}")
    try:
        result = run_rag_query(request.question)
        
        answer = result.get("result", "")
        source_docs = result.get("source_documents", [])
        is_fallback = result.get("is_fallback", False)
        
        sources = list(set([
            str(doc.metadata.get("source", ""))
            for doc in source_docs
        ]))
        
        print(f"DEBUG: Answer obtained (fallback={is_fallback}): {answer[:100]}...")
        if sources:
            print(f"DEBUG: Sources used: {sources}")

        return {
            "answer": answer,
            "sources": sources,
            "is_fallback": is_fallback
        }

    except Exception as e:
        import logging
        import traceback
        error_msg = f"Error during query: {str(e)}\n{traceback.format_exc()}"
        logging.error(error_msg)
        print(f"ERROR: {error_msg}")
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")
