from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from app.services.vector_store import get_vector_store
import os

def get_llm():
    """
    Returns LLM with OpenAI as primary and Gemini as fallback
    """
    # Try OpenAI first
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        try:
            from app.services.openai_wrapper import CustomOpenAILLM
            print("DEBUG: Using OpenAI LLM (gpt-4o-mini)")
            return CustomOpenAILLM(model="gpt-4o-mini", temperature=0.1)
        except Exception as e:
            print(f"WARNING: OpenAI LLM failed: {e}. Falling back to Gemini...")
    
    # Fallback to Gemini
    gemini_key = os.getenv("GOOGLE_API_KEY")
    if gemini_key:
        try:
            from app.services.gemini_wrapper import CustomGeminiLLM
            print("DEBUG: Using Gemini LLM (gemini-2.0-flash)")
            return CustomGeminiLLM(gemini_model="gemini-2.0-flash", temperature=0.1)
        except Exception as e:
            print(f"ERROR: Gemini LLM also failed: {e}")
            raise Exception("Both OpenAI and Gemini LLMs failed. Please check your API keys.")
    
    raise Exception("No API keys found. Please set OPENAI_API_KEY or GOOGLE_API_KEY in your .env file")

def get_rag_chain():
    """
    Creates a RAG chain with LLM fallback support
    """
    llm = get_llm()

    vector_db = get_vector_store()
    retriever = vector_db.as_retriever(search_kwargs={"k": 5})

    template = """You are a helpful assistant that answers questions based ONLY on the provided context.
If the answer is not contained in the context, say "I don't know" or "The provided context does not contain this information."
Do not describe the context, do not mention "the provided context", and do not explain your reasoning.
Just provide the direct answer based strictly on the content below.

Context: {context}

Question: {question}

Helpful Answer:"""
    
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
    )

    return qa
def run_rag_query(question: str):
    """
    Executes a RAG query and handles smart fallback if context is missing
    """
    qa = get_rag_chain()
    
    print(f"DEBUG: Executing RAG chain for: {question}")
    result = qa.invoke({"query": question})
    
    answer = result.get("result", "").strip()
    source_docs = result.get("source_documents", [])
    
    # Check if we got an "I don't know" style answer
    check_phrase = answer.lower()
    is_idk = any(phrase in check_phrase for phrase in [
        "i don't know", 
        "i do not know", 
        "context does not contain",
        "no information",
        "not mentioned in the context"
    ])
    
    if is_idk:
        print("DEBUG: RAG context insufficient. Triggering smart fallback to general knowledge...")
        llm = get_llm()
        
        # Simple generic fallback prompt
        fallback_prompt = f"""You are a helpful AI assistant. The user asked: "{question}"
Provide a helpful, accurate answer based on your general knowledge.
Keep it concise and professional."""
        
        fallback_answer = llm.invoke(fallback_prompt)
        
        return {
            "result": fallback_answer,
            "source_documents": [], # Empty list since it's from general knowledge
            "is_fallback": True
        }
        
    return {
        "result": answer,
        "source_documents": source_docs,
        "is_fallback": False
    }
