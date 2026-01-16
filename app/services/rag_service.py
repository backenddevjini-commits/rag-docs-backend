from app.core.llm import LLMClient
from app.services.embedding import embed_text
from app.core.config import settings
from app.db.vector_store import FaissVectorStore
from typing import List, Dict

class RagService:
    def __init__(self):
        self.vector_store = FaissVectorStore(dim=settings.EMBEDDING_DIM)
        self.llm = LLMClient()

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
    
    def build_prompt(self, question: str, docs: List[Dict]) -> str:
        context = "\n\n".join(
            f" - {d['text']}" for d in docs
        )

        return f"""
    아래 문서를 참고하여 질문에 답변하시오.
    문서에 없는 내용은 답하지 마시오.

    [문서]
    {context}

    [질문]
    {question}
    """.strip()

    def answer(self, question: str) -> str:
        docs = self.retrieve(question)
        prompt = self.build_prompt(question, docs)
        return self.llm.generate(prompt)
        
if __name__ == "__main__":
    rag = RagService()
    answer = rag.answer("RAG의 핵심 구성 요소는 무엇인가?")
    print(answer)