from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

print(settings.OPENAI_API_KEY[:10])

def embed_text(text: str) -> list:
    """
    하나의 텍스트를 embedding 벡터로 변환
    """
    if not text:
        return []
    
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding

if __name__ == "__main__":
    sample = "RAG 기반 문서 Q&A 테스트 문장입니다."
    vector = embed_text(sample)

    print(type(vector))
    print(len(vector))
    print(vector[:5])