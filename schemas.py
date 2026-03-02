from pydantic import BaseModel, Field
from typing import Optional, List


class QueryRequest(BaseModel):
    query: str = Field(..., example="What are Vamsi's technical skills?")
    top_k: Optional[int] = Field(default=3, ge=1, le=10)


class ChunkResult(BaseModel):
    key: str
    text: str
    score: float


class QueryResponse(BaseModel):
    query: str
    top_category: str
    retrieved_chunks: List[ChunkResult]
    context: str


class HealthResponse(BaseModel):
    status: str
    server: str
    total_chunks: int
