from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.crawl import router as crawl_router
from app.api.query import router as query_router

app = FastAPI(title="WebCrawlRAG Backend")

# ✅ CORS CONFIG (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Backend running"}

app.include_router(crawl_router, prefix="/api")
app.include_router(query_router, prefix="/api")
