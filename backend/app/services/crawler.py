import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def crawl_url(url: str) -> dict:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        # Remove unwanted tags
        for tag in soup(["script", "style", "noscript", "header", "footer"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        # Clean whitespace
        clean_text = " ".join(text.split())

        return {
            "url": url,
            "domain": urlparse(url).netloc,
            "content": clean_text[:100000]  # Increased limit
        }

    except Exception as e:
        return {
            "url": url,
            "error": str(e)
        }
