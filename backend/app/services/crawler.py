import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def crawl_url(url: str) -> dict:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        # Remove unwanted tags
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ")

        # Clean whitespace
        clean_text = " ".join(text.split())

        return {
            "url": url,
            "domain": urlparse(url).netloc,
            "content": clean_text[:5000]  # safety limit for now
        }

    except Exception as e:
        return {
            "url": url,
            "error": str(e)
        }
