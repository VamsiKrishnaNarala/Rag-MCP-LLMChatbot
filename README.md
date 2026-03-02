# 🤖 Vamsi Resume MCP Server

> A **RAG-powered MCP Server** that answers natural language questions about Vamsi Krishna's resume using semantic search — built with FastAPI, FAISS, and Sentence Transformers.

---

## 📌 What is this?

This project exposes resume data as a **queryable API** using the **Model Context Protocol (MCP)**. Instead of keyword matching, it uses **vector embeddings + FAISS** to semantically understand questions and retrieve the most relevant resume sections.

**Example:**
```
Query  → "Where has Vamsi worked as an intern?"
Answer → Returns chunks about AnantaNetra, Celebal, Monkify.ai, Tattavit internships
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT                               │
│          (Swagger UI / curl / Claude Desktop)               │
└─────────────────────┬───────────────────────────────────────┘
                      │  POST /mcp/query
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Server (main.py)                  │
│                                                             │
│   ┌─────────────┐        ┌──────────────────────────────┐  │
│   │  /mcp/query │───────▶│        RAG Engine            │  │
│   │  /mcp/health│        │        (engine.py)           │  │
│   │  /mcp/chunks│        └──────────────┬───────────────┘  │
│   └─────────────┘                       │                  │
│      routes.py                          ▼                  │
│      schemas.py               ┌──────────────────┐        │
│                                │   Vector Store   │        │
│                                │ (vector_store.py)│        │
│                                └────────┬─────────┘        │
└─────────────────────────────────────────┼──────────────────┘
                                          │
                    ┌─────────────────────┼──────────────────┐
                    │                     │                  │
                    ▼                     ▼                  ▼
          ┌──────────────┐   ┌─────────────────────┐  ┌──────────────┐
          │  chunker.py  │   │ Sentence Transformers│  │    FAISS     │
          │              │   │  all-MiniLM-L6-v2   │  │ IndexFlatIP  │
          └──────┬───────┘   └─────────────────────┘  └──────────────┘
                 │
                 ▼
       ┌──────────────────┐
       │  resume_data.py  │
       │                  │
       │  • personal      │
       │  • skills        │
       │  • education     │
       │  • experience    │
       │  • projects      │
       │  • certifications│
       │  • achievements  │
       └──────────────────┘
```

---

## 🔄 Request Flow

```
User Query
    │
    ▼
POST /mcp/query  {"query": "What are Vamsi's LLM skills?", "top_k": 3}
    │
    ▼
Encode query → 384-dim vector  (Sentence Transformers)
    │
    ▼
FAISS Cosine Similarity Search → Top-K matching chunks
    │
    ▼
Return { query, retrieved_chunks, context, top_category }
```

---

## 📁 File Structure

```
project/
├── main.py            ← FastAPI app entry point
├── resume_data.py     ← Resume data as Python dict
├── chunker.py         ← Converts resume dict → text chunks
├── vector_store.py    ← FAISS index + cosine similarity search
├── engine.py          ← RAG pipeline (retrieve + build context)
├── schemas.py         ← Pydantic request/response models
├── routes.py          ← API route handlers
├── requirements.txt   ← Python dependencies
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/resume-mcp-server.git
cd resume-mcp-server
```

### 2. Create virtual environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the server
```bash
uvicorn main:app --reload --port 8000
```

### 5. Open Swagger UI
```
http://127.0.0.1:8000/docs
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Server info |
| `GET` | `/mcp/health` | Health check + total chunks |
| `POST` | `/mcp/query` | Semantic query over resume |
| `GET` | `/mcp/chunks` | List all embedded chunks (debug) |

---

## 🧪 Sample Queries

```bash
# Skills
curl -X POST http://127.0.0.1:8000/mcp/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are Vamsi LLM skills?", "top_k": 3}'

# Experience
curl -X POST http://127.0.0.1:8000/mcp/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Where has Vamsi interned?", "top_k": 3}'

# Projects
curl -X POST http://127.0.0.1:8000/mcp/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Tell me about Vamsi RAG project", "top_k": 2}'

# Education
curl -X POST http://127.0.0.1:8000/mcp/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Vamsi educational background?", "top_k": 2}'
```

### Sample Response
```json
{
  "query": "What are Vamsi LLM skills?",
  "top_category": "skills",
  "retrieved_chunks": [
    {
      "key": "skills",
      "text": "Vamsi's Large Language Models skills: BERT, DistilBERT, RoBERTa, T5, Flan-T5, GPT-3, LLaMA 2, Mistral, Claude 3, Qwen.",
      "score": 0.8923
    }
  ],
  "context": "Vamsi's Large Language Models skills: BERT, DistilBERT..."
}
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| API Framework | FastAPI |
| Embedding Model | `all-MiniLM-L6-v2` (Sentence Transformers) |
| Vector Search | FAISS (IndexFlatIP — cosine similarity) |
| Data Validation | Pydantic v2 |
| Server | Uvicorn |
| Protocol | MCP (Model Context Protocol) |

---

---

## 👤 About

**Narala Vamsi Krishna**
M.Tech in CS (AIML) — JNTUK, Kakinada
📧 vamsikrishnanarala104@gmail.com
📍 Konaseema, Andhra Pradesh
