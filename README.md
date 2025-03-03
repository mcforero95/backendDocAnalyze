# 📄 Backend de Análisis de Documentos con LLM

Proyecto de análisis, resumen y consulta de documentos usando FastAPI y modelos LLM locales.

## 🚀 Tecnologías

- Python 3.10
- FastAPI
- PostgreSQL
- Redis
- Llama.cpp
- Docker y Docker Compose

## 🛠️ Instalación y Ejecución

### Requisitos
- Docker
- Docker Compose
- Modelo LLM en formato `.gguf`

### Configuración
Crea un archivo `.env` con las siguientes variables:

```env
# Base de datos PostgreSQL
DATABASE_URL=postgresql://postgres:<CONTRASEÑA>@<IP_CLOUD_SQL>:5432/analyze_db
POSTGRES_DB=analyze_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<CONTRASEÑA>
POSTGRES_HOST=<IP_CLOUD_SQL>
POSTGRES_PORT=5432

# Redis podría quedar igual si es local
REDIS_URL=redis://redis:6379/0


# Seguridad JWT
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Ruta del modelo LLM local
LLM_MODEL_PATH=./models/llama.gguf

# Redis (para Celery)
REDIS_URL=redis://redis:6379/0
