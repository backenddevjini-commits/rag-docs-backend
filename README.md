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
<img width="413" height="352" alt="Image" src="https://github.com/user-attachments/assets/63301600-3632-4a16-bd03-41b89c61da88" />
