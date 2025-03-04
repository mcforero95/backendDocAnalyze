import secrets
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    LLM_MODEL_PATH: str 
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
