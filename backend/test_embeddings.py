from langchain_community.embeddings import OllamaEmbeddings

try:
    print("Testing OllamaEmbeddings connection...")
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
        base_url="http://localhost:11434"
    )
    
    # Try to embed a simple test
    result = embeddings.embed_query("test")
    print(f"✅ Embedding successful! Vector length: {len(result)}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
