import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

# Load .env
env_path = Path(__file__).parent / ".env"
print(f"Loading .env from: {env_path}")
print(f".env exists: {env_path.exists()}")

load_dotenv(dotenv_path=env_path)

# Check environment variables
openai_key = os.getenv("OPENAI_API_KEY")
google_key = os.getenv("GOOGLE_API_KEY")

print(f"\nOPENAI_API_KEY: {'SET' if openai_key else 'NOT SET'}")
if openai_key:
    print(f"  Value: {openai_key[:10]}... (length: {len(openai_key)})")
    
print(f"\nGOOGLE_API_KEY: {'SET' if google_key else 'NOT SET'}")
if google_key:
    print(f"  Value: {google_key[:10]}... (length: {len(google_key)})")

# Try to initialize embeddings
print("\n--- Testing Embedding Initialization ---")
try:
    from app.services.vector_store import get_embedding_function
    embeddings = get_embedding_function()
    print(f"✅ Embeddings initialized successfully: {type(embeddings).__name__}")
except Exception as e:
    print(f"❌ Embeddings initialization failed: {e}")
    import traceback
    traceback.print_exc()
