from langchain_community.vectorstores import Chroma
import os

def get_embedding_function():
    """
    Returns embedding function with OpenAI as primary and Gemini as fallback
    """
    # Try OpenAI first
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        try:
            from app.services.openai_wrapper import CustomOpenAIEmbeddings
            print("DEBUG: Using OpenAI embeddings (text-embedding-3-small)")
            return CustomOpenAIEmbeddings(model="text-embedding-3-small")
        except Exception as e:
            print(f"WARNING: OpenAI embeddings failed: {e}. Falling back to Gemini...")
    
    # Fallback to Gemini
    gemini_key = os.getenv("GOOGLE_API_KEY")
    if gemini_key:
        try:
            from app.services.gemini_wrapper import CustomGeminiEmbeddings
            print("DEBUG: Using Gemini embeddings (text-embedding-004)")
            return CustomGeminiEmbeddings()
        except Exception as e:
            print(f"ERROR: Gemini embeddings also failed: {e}")
            raise Exception("Both OpenAI and Gemini embeddings failed. Please check your API keys.")
    
    raise Exception("No API keys found. Please set OPENAI_API_KEY or GOOGLE_API_KEY in your .env file")

def get_vector_store():
    """
    Returns a persistent ChromaDB vector store
    """
    persist_dir = os.path.join(os.getcwd(), "chroma_db")
    print(f"DEBUG: Initializing ChromaDB at {persist_dir}")
    
    embedding_function = get_embedding_function()
    
    return Chroma(
        persist_directory=persist_dir,
        embedding_function=embedding_function
    )
