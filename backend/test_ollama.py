import requests

try:
    response = requests.get("http://localhost:11434/api/tags")
    print("✅ Ollama is accessible!")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"❌ Error connecting to Ollama: {e}")
