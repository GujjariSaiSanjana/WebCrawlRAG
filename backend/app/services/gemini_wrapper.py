import os
import requests
import json
import time
from typing import List, Optional, Any, Dict, Mapping
from langchain.llms.base import LLM
from langchain.embeddings.base import Embeddings

class CustomGeminiEmbeddings(Embeddings):
    """Custom Embeddings wrapper using Gemini's REST API with Batch Support."""
    
    def __init__(self, gemini_model: str = "models/text-embedding-004", google_api_key: str = None):
        key = google_api_key or os.getenv("GOOGLE_API_KEY")
        self.api_key = key.strip() if key else ""
        self.model_name = gemini_model if gemini_model.startswith("models/") else f"models/{gemini_model}"
        # Use v1beta for batchEmbedContents
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embeds a list of documents using batch requests to save quota."""
        if not texts:
            return []
            
        results = []
        # Gemini batch limit is 100 per request
        batch_size = 50 
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            payload = {
                "requests": [
                    {
                        "model": self.model_name,
                        "content": {"parts": [{"text": text}]}
                    }
                    for text in batch
                ]
            }
            url = f"{self.base_url}/{self.model_name}:batchEmbedContents?key={self.api_key}"
            headers = {'Content-Type': 'application/json'}
            
            success = False
            for attempt in range(10):
                try:
                    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
                    if response.status_code == 200:
                        batch_embeddings = [e["values"] for e in response.json()["embeddings"]]
                        results.extend(batch_embeddings)
                        success = True
                        break
                    elif response.status_code == 429:
                        wait = (attempt + 1) * 10
                        print(f"DEBUG: 429 Rate Limit (Batch Embed). Waiting {wait}s...")
                        time.sleep(wait)
                    else:
                        raise Exception(f"Gemini API Error {response.status_code}: {response.text}")
                except Exception as e:
                    if attempt == 9: raise e
                    time.sleep(5)
            
            if not success:
                raise Exception("Failed to embed documents after multiple retries.")
            
            # small delay between batches to be safe
            if i + batch_size < len(texts):
                time.sleep(2)
                
        return results

    def embed_query(self, text: str) -> List[float]:
        """Embeds a single query."""
        url = f"{self.base_url}/{self.model_name}:embedContent?key={self.api_key}"
        payload = {
            "model": self.model_name,
            "content": {"parts": [{"text": text}]}
        }
        headers = {'Content-Type': 'application/json'}
        
        for attempt in range(5):
            try:
                response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
                if response.status_code == 200:
                    return response.json()["embedding"]["values"]
                elif response.status_code == 429:
                    time.sleep(5)
                else:
                    raise Exception(f"Gemini API Error {response.status_code}: {response.text}")
            except Exception as e:
                if attempt == 4: raise e
                time.sleep(2)
        return []

class CustomGeminiLLM(LLM):
    """Custom LLM wrapper using Gemini's REST API."""
    
    gemini_model: str = "gemini-2.0-flash"
    api_key: Optional[str] = None
    temperature: float = 0.1

    @property
    def _llm_type(self) -> str:
        return "custom_gemini"

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"gemini_model": self.gemini_model, "temperature": self.temperature}

    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs: Any) -> str:
        raw_key = getattr(self, "api_key", None) or os.getenv("GOOGLE_API_KEY")
        key = str(raw_key).strip() if raw_key else ""
        
        model_part = str(self.gemini_model)
        if not model_part.startswith("models/"):
            model_part = f"models/{model_part}"
            
        url = f"https://generativelanguage.googleapis.com/v1beta/{model_part}:generateContent?key={key}"
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": self.temperature,
            }
        }
        headers = {'Content-Type': 'application/json'}

        for attempt in range(6): # Fast retries, focusing on the 1-minute window
            try:
                response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
                if response.status_code == 200:
                    data = response.json()
                    if 'candidates' in data and data['candidates']:
                        candidate = data['candidates'][0]
                        if candidate.get('finishReason') == 'SAFETY':
                            return "I cannot answer this question due to safety filters."
                        return candidate['content']['parts'][0]['text']
                    else:
                        return "The AI returned an empty response."
                elif response.status_code == 429:
                    wait_time = 25 # Standard wait to let a portion of the window clear
                    print(f"DEBUG: 429 Rate Limit. Waiting {wait_time}s (Attempt {attempt+1}/6)...")
                    time.sleep(wait_time)
                else:
                    return f"API Error {response.status_code}: {response.text}"
            except Exception as e:
                if attempt == 5: raise e
                time.sleep(5)
        
        return "The system is currently rate-limited by Google Gemini. Please wait about 30 seconds and try again."
