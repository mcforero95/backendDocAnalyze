
# 📄 Backend y Frontend de Análisis de Documentos con LLM

Proyecto para análisis, resumen y consulta de documentos utilizando FastAPI, modelos LLM locales y un frontend web.

## 🚀 Tecnologías utilizadas

- **Backend:** Python 3.10, FastAPI, PostgreSQL, Redis, Llama.cpp.
- **Orquestación:** Docker y Docker Compose.

## 🛠️ Instalación y ejecución local

### ✅ Requisitos previos

- Docker
- Docker Compose
- Modelo LLM en formato `.gguf` (Por ejemplo, **Mistral q4_k_m**).  
  ⚠️ *No incluido en el repositorio debido al peso. Debes descargarlo y colocarlo en la carpeta `/models` del backend.*
- Link Descarga: https://drive.google.com/drive/folders/1967CAd9-_iccfcjFwj5eDRVjiIz6W8tx

### ✅ Clonar el repositorio y preparar el entorno

1. Clona los repositorios del backend y frontend dentro de la carpeta uniandesRepo.
2. Ubica el modelo `.gguf` en:
   ```
   /backendDocAnalyze/models/mistral.gguf
   ```

3. Crea el archivo `.env` con las siguientes variables:

```env
DATABASE_URL=postgresql://postgres:analyzedb@postgres:5432/analyze_db
POSTGRES_DB=analyze_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=analyzedb
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
LLM_MODEL_PATH=./models/mistral.gguf
REDIS_URL=redis://redis:6379/0
```

### ✅ Construcción y ejecución

Desde la carpeta del backend (`backendDocAnalyze/`):

#### 🔹 Construir los contenedores:
```bash
docker-compose build --no-cache
```

#### 🔹 Levantar los contenedores:
```bash
docker-compose up -d
```

#### 🔹 Ver logs en tiempo real del backend:
```bash
docker logs -f backend_doc_analyze
```

#### 🔹 Detener todos los contenedores:
```bash
docker-compose down
```

#### 🔹 Limpiar contenedores e imágenes:
```bash
docker system prune -a
```

### ✅ Alembic (migración de base de datos)

#### 🔹 Primer uso:

1. Accede al backend:
    ```bash
    docker exec -it backend_doc_analyze bash
    ```

2. Crea la carpeta de migraciones (si no existe):
    ```bash
    mkdir -p /app/alembic/versions
    ```

3. Genera la migración inicial:
    ```bash
    alembic revision --autogenerate -m "Initial migration"
    alembic upgrade head
    ```

## 🌐 Accesos

- **Frontend:** http://localhost:80/
- **Backend (FastAPI docs):** http://localhost:8000/docs

## ⚠️ Uso de recursos

Por defecto, los contenedores utilizan **todos los recursos disponibles** (CPU y RAM) de la máquina donde se ejecuten.  
Si se requiere limitar los recursos, se debe modificar manualmente el archivo `docker-compose.yml` añadiendo el bloque `deploy.resources.limits`.
