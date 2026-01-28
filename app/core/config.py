from pydantic import BaseSettings


class Settings(BaseSettings):
    # DB
    DATABASE_URL: str = "sqlite:///./test.db"

    # OpenAI
    OPENAI_API_KEY: str

    # Logging
    LOG_LEVEL: str = "INFO"

    EMBEDDING_DIM: int = 1536  # OpenAI text-embedding-3-small 기준

    DISTANCE_THRESHOLD: float = 1.0

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
    

settings = Settings()
