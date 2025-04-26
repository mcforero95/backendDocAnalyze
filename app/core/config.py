import secrets
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # --- Base de datos ---
    DATABASE_URL: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    # --- Seguridad ---
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # --- Archivos compartidos (ya no NFS) ---
    SHARED_FILES_PATH: str  # Lo vamos a eliminar progresivamente en el resto del código

    # --- Integraciones IA ---
    GEMINI_API_KEY: str
    GEMINI_MODEL_NAME: str

    # --- Redis (si se sigue usando) ---
    REDIS_URL: str

    # --- Nuevas variables GCP ---
    GCP_PROJECT_ID: str
    CLOUD_STORAGE_BUCKET: str
    PUBSUB_TOPIC: str
    PUBSUB_SUBSCRIPTION: str

    # Se genera dinámicamente cada vez
    @property
    def SECRET_KEY(self):
        return secrets.token_hex(32)

    class Config:
        env_file = ".env"

settings = Settings()

# Alias útiles
SQLALCHEMY_DATABASE_URI = (
    f"postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)
