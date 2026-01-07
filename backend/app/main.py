from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.crawl import router as crawl_router
from app.api.query import router as query_router

app = FastAPI(title="WebCrawlRAG Backend")

# ✅ CORS CONFIG (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Backend running"}

app.include_router(crawl_router, prefix="/api")
app.include_router(query_router, prefix="/api")
