"""
Vamsi Resume MCP Server
Run: uvicorn main:app --reload --port 8000
Docs: http://127.0.0.1:8000/docs
"""

import sys
import os

# Add project root to path so all submodules are found
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from resume_data import resume_memory
from engine import RAGEngine
from routes import router, set_engine

app = FastAPI(
    title="Vamsi Resume MCP Server",
    description="RAG-powered MCP server for querying Vamsi's resume semantically.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    print("[Startup] Initializing RAG engine...")
    engine = RAGEngine(resume_memory)
    set_engine(engine)
    print("[Startup] RAG engine ready.")

app.include_router(router, prefix="/mcp")

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Vamsi Resume MCP Server is running.",
        "docs": "/docs",
        "query_endpoint": "/mcp/query"
    }
