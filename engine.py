"""
RAG Engine: retrieves relevant resume chunks.
"""

from vector_store import ResumeVectorStore


class RAGEngine:
    def __init__(self, resume_data: dict):
        self.store = ResumeVectorStore(resume_data)

    def retrieve(self, query: str, top_k: int = 3) -> list:
        return self.store.search(query, top_k=top_k)

    def build_context(self, chunks: list) -> str:
        return "\n\n".join([c["text"] for c in chunks])

    def query(self, user_query: str, top_k: int = 3) -> dict:
        chunks = self.retrieve(user_query, top_k=top_k)
        context = self.build_context(chunks)

        return {
            "query": user_query,
            "retrieved_chunks": chunks,
            "context": context,
            "top_category": chunks[0]["key"] if chunks else "unknown"
        }
