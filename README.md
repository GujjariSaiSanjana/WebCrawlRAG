# WebCrawlRAG - Intelligent Web Content Q&A System

A powerful RAG (Retrieval-Augmented Generation) system that crawls websites, stores content in a vector database, and answers questions based on the crawled information using AI.

## 🌟 Features

- **Web Crawling**: Automatically crawl and extract content from any website
- **Vector Storage**: Efficient storage using ChromaDB for semantic search
- **AI-Powered Q&A**: Get accurate answers based on crawled content
- **Dual LLM Support**: OpenAI (primary) with Gemini (fallback) for maximum reliability
- **Modern UI**: Clean Next.js frontend for easy interaction
- **Docker Ready**: Fully containerized for easy deployment

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Frontend  │─────▶│   Backend    │─────▶│  ChromaDB   │
│  (Next.js)  │      │  (FastAPI)   │      │  (Vectors)  │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  LLM APIs    │
                     │ OpenAI/Gemini│
                     └──────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- At least one API key:
  - **OpenAI API Key** (recommended): Get from [OpenAI Platform](https://platform.openai.com/api-keys)
  - **Google Gemini API Key** (fallback): Get from [Google AI Studio](https://aistudio.google.com/app/apikey)

### Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd WebCrawlRAG
   ```

2. **Configure API Keys**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your API keys
   # You need at least one key (OpenAI recommended)
   ```

3. **Start the application**
   ```bash
   docker compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3001
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 📖 Usage

### 1. Crawl Websites

Use the frontend or send a POST request to crawl websites:

```bash
curl -X POST http://localhost:8000/api/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://example.com", "https://another-site.com"]
  }'
```

### 2. Ask Questions

Query the crawled content:

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the main topic of the crawled websites?"
  }'
```

## 🔧 Configuration

### LLM Provider Priority

The system uses a fallback mechanism:
1. **OpenAI** (if `OPENAI_API_KEY` is set)
   - LLM: `gpt-4o-mini`
   - Embeddings: `text-embedding-3-small`
2. **Gemini** (if OpenAI fails or `GOOGLE_API_KEY` is set)
   - LLM: `gemini-2.0-flash`
   - Embeddings: `text-embedding-004`

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key (primary) | At least one |
| `GOOGLE_API_KEY` | Google Gemini API key (fallback) | At least one |

## 🛠️ Development

### Running Locally (without Docker)

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Project Structure

```
WebCrawlRAG/
├── backend/
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── services/      # Business logic
│   │   │   ├── openai_wrapper.py    # OpenAI integration
│   │   │   ├── gemini_wrapper.py    # Gemini integration
│   │   │   ├── rag_chain.py         # RAG orchestration
│   │   │   └── vector_store.py      # ChromaDB interface
│   │   └── main.py        # FastAPI app
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/              # Next.js frontend
├── docker-compose.yml
└── .env.example
```

## 🎯 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/api/crawl` | POST | Crawl and store website content |
| `/api/query` | POST | Query the knowledge base |
| `/docs` | GET | Interactive API documentation |

## 🔍 How It Works

1. **Crawling**: The system fetches web pages and extracts text content
2. **Chunking**: Content is split into manageable chunks
3. **Embedding**: Each chunk is converted to a vector using OpenAI/Gemini embeddings
4. **Storage**: Vectors are stored in ChromaDB for efficient retrieval
5. **Querying**: User questions are embedded and matched against stored vectors
6. **Generation**: Relevant chunks are sent to the LLM to generate accurate answers

## 💡 Tips

- **API Costs**: OpenAI has usage-based pricing. Gemini offers a generous free tier.
- **Crawling**: Be respectful of websites' robots.txt and rate limits
- **Persistence**: ChromaDB data persists in the `chroma_db` directory
- **Scaling**: For production, consider using a managed vector database

## 🐛 Troubleshooting

**"No API keys found" error:**
- Ensure your `.env` file exists and contains at least one valid API key
- Restart Docker containers after updating `.env`

**Crawling fails:**
- Check if the target website is accessible
- Some sites may block automated crawling

**Slow responses:**
- First query may be slower as models initialize
- Consider using OpenAI for faster responses

## 📝 License

MIT License - feel free to use this project for your own purposes!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
