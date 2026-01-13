"""
FAISS 기반 벡터 저장소
- 임베딩 벡터를 FAISS index로 저장
- 벡터와 metadata를 같은 순서로 관리
- 서버 재시작 후에도 재사용 가능하도록 파일로 유지
"""

import faiss
import json
import numpy as np
from pathlib import Path
from typing import List, Dict

class FaissVectorStore:
    """
    FAISS 벡터 저장소 클래스

    역할:
    1. FAISS index 생성 / 로드
    2. embedding 벡터 추가
    3. metadata(원문, 출처 등) 관리
    4. 검색 시 벡터 결과를 원문으로 매핑
    """

    def __init__(
        self,
        dim: int,
        index_path: str = "storage/index.faiss",
        metadata_path: str = "storage/metadata.json"
    ):
        """
        [1] 초기화 단계

        - embedding 차원(dim)을 고정
        - 기존 index 파일이 있으면 로드
        - 없으면 새 FAISS index 생성
        """
        self.dim = dim
        self.index_path = Path(index_path)
        self.metadata_path = Path(metadata_path)

        # index 파일이 저장될 디렉토리 생성
        self.index_path.parent.mkdir(parents=True, exist_ok=True)

        if self.index_path.exists():
            # 기존 index 재사용 (재시작 대응)
            self.index = faiss.read_index(str(self.index_path))
            self.metadata = self._load_metadata()
        else:
            # 최초 실행 시 새 index 생성
            self.index = faiss.IndexFlatL2(dim)
            self.metadata: List[Dict] = []
    
    def add(self, embeddings: List[List[float]], metadatas: List[Dict]):
        """
        [2] 벡터 & 메타데이터 추가 단계

        - embeddings: chunk 임베딩 결과
        - metadatas: 각 chunk의 원문 정보
        - 두 리스트의 순서는 반드시 동일해야함
        """
        vectors = np.array(embeddings).astype("float32")

        # embedding 차원 검증 (실수 방지용)
        if vectors.shape[1] != self.dim:
            raise ValueError("Embedding dimension mismatch")
        
        # FAISS index에 벡터 추가
        self.index.add(vectors)

        # 벡터 순서와 동일하게 metadata 저장
        self.metadata.extend(metadatas)

    def save(self):
        """
        [3] 저장 단계

        - FAISS index -> .faiss 파일
        - metadata -> json 파일
        """
        faiss.write_index(self.index, str(self.index_path))
        self._save_metadata()

    def search(self, query_embedding: List[float], k: int = 5):
        """
        [4] 검색 단계

        - query_embedding으로 FAISS 검색
        - top-k 결과의 index를 이용해 metadata 반환
        """
        q = np.array([query_embedding]).astype("float32")

        distance, indices = self.index.search(q, k)

        results = []
        for idx in indices[0]:
            if idx == -1:
                continue
            results.append(self.metadata[idx])

        return results
    
    def _save_metadata(self):
        """
        [5] metadata 저장 (내부 메서드)

        - FAISS는 벡터만 저장하므로 원문 텍스트 / 출처 정보는 별도 파일로 관리
        """
        with open(self.metadata_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)

    def _load_metadata(self):
        """
        [6] metadata 로드 (내부 메서드)

        - index와 metadata 순서가 어긋나면 안 되므로 항상 함께 로드
        """
        if not self.metadata_path.exists():
            return []
        
        with open(self.metadata_path, "r", encoding="utf-8") as f:
            return json.load(f)

if __name__ == "__main__":
    from app.services.embedding import embed_text

    # 🔹 기존 index + metadata 로드
    store = FaissVectorStore(dim=1536)  # text-embedding-3-small 기준

    query = "이 문서의 주요 내용은 무엇인가?"
    query_embedding = embed_text(query)

    results = store.search(query_embedding, k=3)

    print("\n=== 검색 결과 ===")
    for i, r in enumerate(results, 1):
        print(f"\n[{i}] source: {r.get('source')}")
        print(r.get("text")[:200])