from fastapi import APIRouter, HTTPException
from schemas import QueryRequest, QueryResponse, HealthResponse

router = APIRouter()

rag_engine = None


def set_engine(engine):
    global rag_engine
    rag_engine = engine


@router.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "server": "Vamsi Resume MCP Server",
        "total_chunks": rag_engine.store.index.ntotal if rag_engine else 0
    }


@router.post("/query", response_model=QueryResponse, tags=["MCP"])
def handle_query(request: QueryRequest):
    if rag_engine is None:
        raise HTTPException(status_code=503, detail="RAG engine not initialized")
    result = rag_engine.query(request.query, top_k=request.top_k)
    return result


@router.get("/chunks", tags=["Debug"])
def list_all_chunks():
    if rag_engine is None:
        raise HTTPException(status_code=503, detail="RAG engine not initialized")
    return {
        "total": len(rag_engine.store.chunks),
        "chunks": rag_engine.store.chunks
    }
