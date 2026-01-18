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
