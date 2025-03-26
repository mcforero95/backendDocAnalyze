
# 📄 Backend y Frontend de Análisis de Documentos con LLM

Proyecto para análisis, resumen y consulta de documentos utilizando FastAPI, recuperación de contexto (RAG), Gemini IA y PostgreSQL.

---

## 🚀 Tecnologías utilizadas

- **Backend:** Python 3.10, FastAPI, PostgreSQL, Alembic
- **LLM:** Gemini IA de Google vía API (antes: llama.cpp con modelo `.gguf`)
- **Embeddings locales:** Sentence Transformers (`all-MiniLM-L6-v2`)
- **Orquestación:** Docker y Docker Compose

---

## 🛠️ Instalación y ejecución local

### ✅ Requisitos previos

- Docker y Docker Compose
- Clave de API de Google para Gemini IA
- Variables de entorno configuradas

### ✅ Variables de entorno

```env
# Base de datos PostgreSQL (nombre del servicio dentro del docker-compose)
DATABASE_URL=postgresql://postgres:analyzedb@postgres:5432/analyze_db
POSTGRES_DB=analyze_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=analyzedb
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Seguridad JWT
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Ruta del modelo de lenguaje`
GEMINI_API_KEY=Aqui tu apikey
GEMINI_MODEL_NAME=gemini-2.0-flash

# Redis (para Celery)
REDIS_URL=redis://redis:6379/0
```

---

## ✅ Construcción y ejecución

```bash
docker-compose build --no-cache
docker-compose up -d
```

Accede a:

- **Frontend:** http://localhost:80/
- **API Docs:** http://localhost:8000/docs

---

## 🧠 Funcionalidades clave

- ✅ Subida de documentos (`.pdf`, `.docx`, `.txt`)
- ✅ Extracción y segmentación del texto en *chunks*
- ✅ Generación de **embeddings** por chunk
- ✅ Resumen del documento usando **Gemini**
- ✅ Chat con el documento vía preguntas/respuestas
- ✅ **Recuperación de Contexto (RAG)** con chunks relevantes
- ✅ Historial de conversaciones y mensajes por usuario

---

## 📌 Cómo usar RAG

### Endpoint:
`POST /ask/{document_id}?rag=true`

### Parámetros:

| Nombre    | Tipo   | Descripción                                 |
|-----------|--------|---------------------------------------------|
| rag       | bool   | (Opcional) Si se usa RAG. Default: false    |

### Body:

| question  | Pregunta del usuario                        |

---

## 🧱 Modelo de datos principal

### 📄 `documents`
- `id`, `title`, `content`, `owner_id`

### 🧩 `document_chunks`
- `id`, `document_id`, `chunk_text`, `embedding`, `chunk_index`

### 💬 `conversations`
- `id`, `user_id`, `document_id`, `created_at`

### 💭 `messages`
- `id`, `conversation_id`, `question`, `answer`, `created_at`

---

## 🧪 Alembic (migración de base de datos)

```bash
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

---

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

## ✅ Exportación de contenedores para compartir

### 🔹 Exportar los contenedores:
```bash
docker save -o backenddocanalyze-frontend.tar backenddocanalyze-frontend:latest
docker save -o backenddocanalyze-app.tar backenddocanalyze-app:latest
docker save -o postgres.tar postgres:16
docker save -o redis.tar redis:7
```

### 🔹 Importación en otra máquina de contenedores:

1. Descargga los contenedores y carga las imágenes:
    ```bash
    docker load -i backenddocanalyze-app.tar
    docker load -i postgres.tar
    docker load -i redis.tar
    docker load -i backenddocanalyze-frontend.tar
    ```

3. Levantar los servicios:
    ```bash
    docker-compose up -d
    ```
