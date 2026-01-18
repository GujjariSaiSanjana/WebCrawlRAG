from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rag_chain import get_rag_chain

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
def ask_question(request: QueryRequest):
    print(f"DEBUG: Received question: {request.question}")
    try:
        qa = get_rag_chain()
        print("DEBUG: Executing RAG chain...")
        result = qa.invoke({"query": request.question})
        print(f"DEBUG: result keys: {list(result.keys())}")
        answer = str(result.get("result", ""))
        source_docs = result.get("source_documents", [])
        sources = list(set([
            str(doc.metadata.get("source", ""))
            for doc in source_docs
        ]))
        
        print(f"DEBUG: Answer obtained: {answer[:100]}...")
        print(f"DEBUG: Sources used: {sources}")

        return {
            "answer": answer,
            "sources": sources
        }

    except Exception as e:
        import logging
        import traceback
        error_msg = f"Error during query: {str(e)}\n{traceback.format_exc()}"
        logging.error(error_msg)
        print(f"ERROR: {error_msg}")
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")
