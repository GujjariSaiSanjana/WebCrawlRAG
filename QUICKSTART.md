# 🚀 Quick Start Guide

## You're Almost Ready!

Your WebCrawlRAG project has been successfully migrated from Ollama to **OpenAI (primary) + Gemini (fallback)**!

## ⚡ 3 Steps to Get Running

### Step 1: Add Your OpenAI API Key

Open the `.env` file and replace the placeholder:

```bash
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

> 💡 Get your key at: https://platform.openai.com/api-keys

### Step 2: Start the Application

```bash
docker compose up --build
```

### Step 3: Test It Out

Open your browser to:
- **Frontend**: http://localhost:3001
- **API Docs**: http://localhost:8000/docs

## 📝 What Changed?

✅ **Removed**: Ollama dependency (no local installation needed)  
✅ **Added**: OpenAI as primary LLM (better quality, faster)  
✅ **Added**: Gemini as automatic fallback (reliability)  
✅ **Created**: Complete documentation and Dockerfile

## 🎯 How It Works Now

1. **OpenAI First**: Uses `gpt-4o-mini` and `text-embedding-3-small`
2. **Gemini Fallback**: Automatically switches if OpenAI fails
3. **No Local Setup**: Everything runs via cloud APIs

## 📚 Need More Info?

- Full documentation: [README.md](file:///c:/Users/sarad/Desktop/MINIPROJECT/WebCrawlRAG/README.md)
- Migration details: [walkthrough.md](file:///C:/Users/sarad/.gemini/antigravity/brain/bbab749b-2ba2-44e8-90ab-8c2e2de300ce/walkthrough.md)

---

**Note**: Your Gemini API key is already configured. The system will work with just Gemini if you don't add an OpenAI key, but OpenAI is recommended for better performance.
