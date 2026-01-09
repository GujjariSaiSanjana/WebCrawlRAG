import ollama
import os

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

client = ollama.Client(host=OLLAMA_BASE_URL)
