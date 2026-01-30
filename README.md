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

## RAG 처리 흐름

1. 사용자가 문서를 업로드하면 텍스트를 추출하고 일정 길이로 분할한다.
2. 각 텍스트 조각은 임베딩 모델을 통해 벡터로 변환된다.
3. 변환된 벡터는 FAISS 벡터 저장소에 저장된다.
4. 사용자의 질문이 들어오면 질문을 임베딩하여 벡터 검색을 수행한다.
5. 검색된 문서를 컨텍스트로 LLM 프롬프트를 구성한다.
6. 문서 관련성이 낮을 경우 답변을 생성하지 않도록 제어한다.
7. LLM은 제공된 문서를 기반으로 최종 답변을 생성한다.

## 🔒 사용자 인증 (JWT)

### 회원가입

**POST /users/signup**

요청 예시:

```json
{
  "email": "user@example.com",
  "password": "비밀번호"
}
```

응답 예시:

```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2026-01-29T06:37:47.037623"
}
```

### 로그인

**POST /users/login**

폼 데이터 (Swagger 기준 OAuth2PasswordRequestForm 사용):

```
username=user@example.com
password=비밀번호
```

응답 예시:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 현재 사용자 조회

**GET /users/me**

헤더:
```
Authorization: Bearer <access_token>
```
응답 예시:

```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2026-01-29T06:37:47.037623"
}
```

### 예외 처리
- 잘못된 토큰/만료 → 401 Unauthorized
- JSON 형식:

```json
{
  "success": false,
  "error": {
    "code": 401,
    "message": "Invalid token"
  }
}
```

- 주의 사항
1. /users/login은 OAuth2PasswordRequestForm 기반이라 Swagger에서는 username 칸에 이메일을 넣어야 함.
2. /users/me 같은 보호 API는 반드시 Authorization 헤더에 Bearer 토큰을 넣어야 함.
3. 모든 HTTPException은 exceptions.py에서 정의한 통일된 JSON 포맷으로 반환됨.