from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
import os

# Embedding model using Ollama
embedding_function = OllamaEmbeddings(
    model="nomic-embed-text"
)

def get_vector_store():
    """
    Returns a persistent ChromaDB vector store
    """
    # Use a relative path or a absolute path that exists
    persist_dir = os.path.join(os.getcwd(), "chroma_db")
    print(f"DEBUG: Initializing ChromaDB at {persist_dir}")
    return Chroma(
        persist_directory=persist_dir,
        embedding_function=embedding_function
    )
