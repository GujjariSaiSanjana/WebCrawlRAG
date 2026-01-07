const BASE_URL = "http://127.0.0.1:8000/api";

export async function crawlUrls(urls: string[]) {
  const res = await fetch(`${BASE_URL}/crawl`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ urls }),
  });
  return res.json();
}

export async function askQuestion(question: string) {
  const res = await fetch(`${BASE_URL}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  return res.json();
}
