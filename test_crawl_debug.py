import requests
import json

url = "http://localhost:8000/api/crawl"
payload = {"urls": ["https://example.com"], "clear": False}

try:
    response = requests.post(url, json=payload, timeout=60)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
