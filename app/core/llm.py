from openai import OpenAI
from app.core.config import settings

class LLMClient:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate(self, prompt: str, temperature: float = 0.2) -> str:
        response = self.client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role": "system", "content": "너는 문서 기반 QA 어시스턴트다."},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content