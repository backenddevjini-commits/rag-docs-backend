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
            f"[문서 {i+1}]\n{d['text']}" for i, d in enumerate(docs)
        )

        return f"""
    너는 주어진 문서만을 기반으로 질문에 답변하는 AI이다.
    문서에 없는 내용은 절대 추측하거나 만들어내지 마라.
    답변할 수 없는 경우 반드시 아래 문장으로만 답하라.

    "문서에 해당 정보가 없습니다."

    [문서]
    {context}

    [질문]
    {question}
    """.strip()

    def generate_answer(self, prompt: str) -> str:
        return self.llm.generate(prompt)

    def answer(self, question: str, temperature: float = 0.2) -> dict:
        docs = self.retrieve(question)

        if not docs:
            return {
                "question": question,
                "answer": "관련 문서를 찾지 못했습니다.",
                "sources": []
            }

        min_distance = min(doc["distance"] for doc in docs)

        if min_distance > settings.DISTANCE_THRESHOLD:
            return {
                "question": question,
                "answer": "문서의 관련성이 낮아 답변할 수 없습니다.",
                "sources": []
            }

        prompt = self.build_prompt(question, docs)
        answer = self.llm.generate(prompt, temperature=temperature)

        return {
            "question": question,
            "answer": answer,
            "temperature": temperature,
            "sources": [
                {"distance": d["distance"]} for d in docs
            ]
        }
        
if __name__ == "__main__":
    rag = RagService()
    question = "RAG의 핵심 구성 요소를 한 문장으로 요약해줘"

    for t in [0.0, 0.3, 0.7]:
        print("\n" + "=" * 50)
        print(f"TEMPERATURE = {t}")

        result = rag.answer(question, temperature=t)

        print("Q:", result["question"])
        print("A:", result["answer"])