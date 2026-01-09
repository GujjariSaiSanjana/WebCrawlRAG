import os
from typing import List, Optional, Any, Mapping
from langchain.llms.base import LLM
from langchain.embeddings.base import Embeddings


class CustomOpenAIEmbeddings(Embeddings):
    """Custom Embeddings wrapper using OpenAI's API."""
    
    def __init__(self, model: str = "text-embedding-3-small", openai_api_key: str = None):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("Please install openai: pip install openai")
        
        key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=key.strip())
        self.model = model
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embeds a list of documents using OpenAI's API."""
        if not texts:
            return []
        
        # OpenAI allows up to 2048 texts per request, but we'll use smaller batches
        batch_size = 100
        results = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            try:
                response = self.client.embeddings.create(
                    model=self.model,
                    input=batch
                )
                batch_embeddings = [item.embedding for item in response.data]
                results.extend(batch_embeddings)
            except Exception as e:
                print(f"ERROR: OpenAI embeddings failed for batch {i//batch_size + 1}: {str(e)}")
                raise
        
        return results
    
    def embed_query(self, text: str) -> List[float]:
        """Embeds a single query using OpenAI's API."""
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=[text]
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"ERROR: OpenAI query embedding failed: {str(e)}")
            raise


class CustomOpenAILLM(LLM):
    """Custom LLM wrapper using OpenAI's Chat API."""
    
    model: str = "gpt-4o-mini"
    api_key: Optional[str] = None
    temperature: float = 0.1
    _client: Any = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("Please install openai: pip install openai")
        
        key = self.api_key or os.getenv("OPENAI_API_KEY")
        if not key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Use a private attribute to avoid Pydantic validation issues
        object.__setattr__(self, "_client", OpenAI(api_key=key.strip()))
    
    @property
    def _llm_type(self) -> str:
        return "custom_openai"
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"model": self.model, "temperature": self.temperature}
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs: Any) -> str:
        """Call OpenAI's Chat API."""
        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                stop=stop
            )
            return response.choices[0].message.content
        except Exception as e:
            error_msg = f"OpenAI API Error: {str(e)}"
            print(f"ERROR: {error_msg}")
            raise Exception(error_msg)
