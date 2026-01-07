from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rag_chain import get_rag_chain

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
def ask_question(request: QueryRequest):
    try:
        qa = get_rag_chain()
        result = qa.invoke({"query": request.question})

        return {
            "answer": result["result"],
            "sources": [
                doc.metadata.get("source", "")
                for doc in result["source_documents"]
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
