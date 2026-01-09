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
        print(f"DEBUG: Answer obtained: {answer[:100]}...")
        print(f"DEBUG: Number of source documents: {len(source_docs)}")

        return {
            "answer": answer,
            "sources": list(set([
                str(doc.metadata.get("source", ""))
                for doc in source_docs
            ]))
        }

    except Exception as e:
        import logging
        import traceback
        error_msg = f"Error during query: {str(e)}\n{traceback.format_exc()}"
        logging.error(error_msg)
        print(f"ERROR: {error_msg}")
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")
