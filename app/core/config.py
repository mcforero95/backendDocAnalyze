import secrets
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    LLM_MODEL_PATH: str = "./models/llama.gguf"
    REDIS_URL: str = "redis://localhost:6379/0"
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    # Se genera dinámicamente cada vez
    @property
    def SECRET_KEY(self):
        return secrets.token_hex(32)

    class Config:
        env_file = ".env"


settings = Settings()
