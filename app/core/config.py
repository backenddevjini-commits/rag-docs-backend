from pydantic import BaseSettings


class Settings(BaseSettings):
    # DB
    DATABASE_URL: str = "sqlite:///./test.db"

    # OpenAI
    OPENAI_API_KEY: str

    # Logging
    LOG_LEVEL: str = "INFO"

    EMBEDDING_DIM: int = 1536  # OpenAI text-embedding-3-small 기준
    class Config:
        env_file = ".env"
    

settings = Settings()
