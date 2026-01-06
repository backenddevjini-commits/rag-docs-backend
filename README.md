# RAG 기반 문서 Q&A 백엔드 서비스

FastAPI 기반 문서 질의응답 API 서버

## 프로젝트 개요

사용자가 업로드한 문서를 기반으로 의미 검색을 수행하고, LLM을 통해 질문에 답변을 제공한다.

### 문제 정의
사내 문서나 매뉴얼이 많아질수록 필요한 정보를 빠르게 찾기 어렵다.

### MVP 범위
##### 🔹 포함
- 문서 업로드 API
- 문서 텍스트 추출
- 임베딩 생성
- 벡터 검색 기반 질의응답

##### 🔹 제외
- 사용자 인증
- 프론트엔드 UI
- 실시간 스트리밍 응답

## 기술 스택
### 🔹 Backend
- Python
- FastAPI
- Uvicorn

### 🔹 LLM / AI
- OpenAI API
- Embedding API

### 🔹 RAG
- Text Splitter
- Embedding
- Vector Search

### 🔹 DB
- Vector DB: FAISS (로컬)
- 메타데이터: SQLite (선택)

### 🔹 기타
- dotenv
- pydantic

## 폴더 구조
app/
 ├─ main.py              # FastAPI 진입점, 라우터 연결
 ├─ routers/             # API 엔드포인트
 │   ├─ health.py        # 서버 상태 체크
 │   ├─ documents.py     # 문서 업로드
 │   └─ qa.py            # 질문 응답
 ├─ services/            # 비즈니스 로직
 │   ├─ loader.py        # 문서 로딩 & 텍스트 추출
 │   ├─ embedding.py     # 임베딩 생성
 │   └─ rag.py           # RAG 통합 로직
 ├─ core/                # 공통 설정 및 환경 변수
 │   ├─ config.py        # 환경 변수 / 설정
 │   └─ llm.py           # llm 호출 관련
 └─ db/
     └─ vector_store.py  # 벡터 DB 관련 (FAISS)