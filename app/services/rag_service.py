from app.services.embedding import embed_text
from app.core.config import settings
from app.db.vector_store import FaissVectorStore
from typing import List

class RagService:
    def __init__(self):
        self.vector_store = FaissVectorStore(dim=settings.EMBEDDING_DIM)

    def retrieve(self, question: str, top_k: int = 3) -> List[str]:
        # 1. 질문 -> embedding
        query_embedding = embed_text(question)

        # 2. FAISS 검색
        results = self.vector_store.search(query_embedding, k=top_k)

        return [
            {
                "distance": r["distance"],
                "text": r["metadata"]["text"]
            }
            for r in results
        ]
        
if __name__ == "__main__":
    rag = RagService()
    docs = rag.retrieve("RAG의 핵심 구성 요소는 무엇인가?")

    for i, d in enumerate(docs, start=1):
        print(f"\n[{i}] distance: {d['distance']:.4f}")
        print(d["text"])