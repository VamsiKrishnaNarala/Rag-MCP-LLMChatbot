"""
Builds a FAISS index from resume chunks and performs semantic search.
"""

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from chunker import build_chunks

# Load embedding model once at startup
EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")


class ResumeVectorStore:
    def __init__(self, resume_data: dict):
        print("[VectorStore] Building chunks...")
        self.chunks = build_chunks(resume_data)
        self.texts = [c["text"] for c in self.chunks]

        print(f"[VectorStore] Embedding {len(self.texts)} chunks...")
        embeddings = EMBED_MODEL.encode(self.texts, show_progress_bar=False)
        embeddings = np.array(embeddings).astype("float32")

        # Normalize for cosine similarity
        faiss.normalize_L2(embeddings)

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings)

        print(f"[VectorStore] Index ready with {self.index.ntotal} vectors.")

    def search(self, query: str, top_k: int = 3) -> list:
        query_vec = EMBED_MODEL.encode([query], show_progress_bar=False)
        query_vec = np.array(query_vec).astype("float32")
        faiss.normalize_L2(query_vec)

        scores, indices = self.index.search(query_vec, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            chunk = self.chunks[idx].copy()
            chunk["score"] = round(float(score), 4)
            results.append(chunk)

        return results
