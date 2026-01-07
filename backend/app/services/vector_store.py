from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

# Embedding model using Ollama
embedding_function = OllamaEmbeddings(
    model="nomic-embed-text"
)

def get_vector_store():
    """
    Returns a persistent ChromaDB vector store
    """
    return Chroma(
        persist_directory="chroma_db",
        embedding_function=embedding_function
    )
