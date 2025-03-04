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
- Modelo LLM en formato `.gguf` este proyecto usa mistral q4 k m el cual no esta en el repo por el peso debes descargarlo y pegarlo en la carpeta models luego de clonar el repo.

### Configuración
Crea un archivo `.env` con las siguientes variables:

# Base de datos PostgreSQL
DATABASE_URL=postgresql://postgres:<CONTRASEÑA>@<IP_CLOUD_SQL o localhost>:5432/analyze_db
POSTGRES_DB=analyze_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<CONTRASEÑA>
POSTGRES_HOST=<IP_CLOUD_SQL o localhost>
POSTGRES_PORT=5432

# Redis podría quedar igual si es local
REDIS_URL=redis://redis:6379/0


# Seguridad JWT
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Ruta del modelo LLM local
LLM_MODEL_PATH=./models/mistral.gguf

# Redis (para Celery)
REDIS_URL=redis://redis:6379/0

### Instalacion de dependecias desde requirements.txt.

# Instala las dependencias 
pip install -r requirements.txt

# Construir los contenedores
docker-compose build

# Subir (iniciar) los contenedores
docker-compose up -d

# Bajar (detener) los contenedores
docker-compose down

# ver log de los contenedores en vivo.

docker logs -f backend_doc_analyze

# eliminar todo el contenedor
docker system prune -a