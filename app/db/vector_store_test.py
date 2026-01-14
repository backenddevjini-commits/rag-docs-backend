from app.db.vector_store import FaissVectorStore
from app.services.embedding import embed_text

store = FaissVectorStore(dim=1536)

# 1. 질문 준비
queries = [
    "RAG의 핵심 구성 요소는 무엇인가?",
    "FAISS는 어떤 역할을 하나?",
    "IndexFlatL2는 무엇인가?"
]


for q_idx, query in enumerate(queries, 1):
    print(f"\n=== 질문 {q_idx} ===")
    print("Q:", query)

    query_embedding = embed_text(query)
    distances, indices = store.index.search(
        # FAISS 내부 search 직접 사용
        # (distance를 보기 위함)
        __import__("numpy").array([query_embedding]).astype("float32"),
        3
    )

    for rank, (d, i) in enumerate(zip(distances[0], indices[0]), 1):
        meta = store.metadata[i]
        print(f"\n[{rank}] distance: {d:.6f}")
        print(meta["text"][:200])