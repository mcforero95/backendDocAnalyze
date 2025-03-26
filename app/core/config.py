import secrets
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    GEMINI_API_KEY: str 
    GEMINI_MODEL_NAME: str
    REDIS_URL: str 
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
