from pydantic import BaseSettings


class Settings(BaseSettings):
    # DB
    DATABASE_URL: str = "sqlite:///./test.db"

    # OpenAI
    OPENAI_API_KEY: str

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()
