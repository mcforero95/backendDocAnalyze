
# 📄 Backend y Frontend de Análisis de Documentos con LLM

Proyecto para análisis, resumen y consulta de documentos utilizando FastAPI, recuperación de contexto (RAG), Gemini IA y PostgreSQL.

---

## 🚀 Tecnologías utilizadas

- **Backend:** Python 3.10, FastAPI, PostgreSQL, Alembic(Para Migración BD)
- **LLM:** Gemini IA de Google vía API Flash 2.0
- **Embeddings locales:** Sentence Transformers (`all-MiniLM-L6-v2`)
- **Orquestación:** Docker y Docker Compose
- **Despliegue:** GCP

---

## 🛠️ Instalación y ejecución local

### ✅ Requisitos previos

- Docker y Docker Compose
- Clave de API de Google para Gemini IA
- Variables de entorno configuradas
- IP VM de la BD.

### ✅ Variables de entorno

```env
# Base de datos PostgreSQL 
DATABASE_URL=postgresql://postgres:analyzedb@<IP VM>:5432/analyze_db
POSTGRES_DB=analyze_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=analyzedb
POSTGRES_HOST=<IP VM>
POSTGRES_PORT=5432

# Ruta de los archivos compartidos nfs
SHARED_FILES_PATH=/mnt/nfs_shared

# Seguridad JWT
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Ruta del modelo de lenguaje`
GEMINI_API_KEY=<Aqui tu apikey>
GEMINI_MODEL_NAME=gemini-2.0-flash

# Redis (para Celery)
REDIS_URL=redis://redis:6379/0
```

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

## 📌 Cómo usar RAG para preguntas al LLM sobre el documento

### Endpoint:
`POST /ask/{document_id}?rag=true`

### Params:
```
| rag       | true                 |
| question  | Pregunta del usuario |
```
---

## 🧱 Modelo de datos principal
```
+------------------+-------------------+---------------------------+----+----+---------------------+
| Tabla            | Columna           | Tipo                      | PK | FK | Referencia          |
+------------------+-------------------+---------------------------+----+----+---------------------+
| alembic_version  | version_num       | character varying         | Y  | N  | —                   |
+------------------+-------------------+---------------------------+----+----+---------------------+
| analysis         | id                | integer                   | Y  | N  | —                   |
| analysis         | document_id       | integer                   | N  | Y  | documents(id)       |
| analysis         | result            | text                      | N  | N  | —                   |
| analysis         | summary           | text                      | N  | N  | —                   |
+------------------+-------------------+---------------------------+----+----+---------------------+
| conversations    | id                | integer                   | Y  | N  | —                   |
| conversations    | user_id           | integer                   | N  | Y  | users(id)           |
| conversations    | document_id       | integer                   | N  | Y  | documents(id)       |
| conversations    | created_at        | timestamp without tz      | N  | N  | —                   |
+------------------+-------------------+---------------------------+----+----+---------------------+
| document_chunks  | id                | integer                   | Y  | N  | —                   |
| document_chunks  | document_id       | integer                   | N  | Y  | documents(id)       |
| document_chunks  | chunk_text        | text                      | N  | N  | —                   |
| document_chunks  | embedding         | json                      | N  | N  | —                   |
| document_chunks  | chunk_index       | integer                   | N  | N  | —                   |
+------------------+-------------------+---------------------------+----+----+---------------------+
| documents        | id                | integer                   | Y  | N  | —                   |
| documents        | title             | character varying         | N  | N  | —                   |
| documents        | content           | character varying         | N  | N  | —                   |
| documents        | owner_id          | integer                   | N  | Y  | users(id)           |
+------------------+-------------------+---------------------------+----+----+---------------------+
| messages         | id                | integer                   | Y  | N  | —                   |
| messages         | conversation_id   | integer                   | N  | Y  | conversations(id)   |
| messages         | question          | text                      | N  | N  | —                   |
| messages         | answer            | text                      | N  | N  | —                   |
| messages         | created_at        | timestamp without tz      | N  | N  | —                   |
+------------------+-------------------+---------------------------+----+----+---------------------+
| users            | id                | integer                   | Y  | N  | —                   |
| users            | username          | character varying         | N  | N  | —                   |
| users            | email             | character varying         | N  | N  | —                   |
| users            | hashed_password   | character varying         | N  | N  | —                   |
+------------------+-------------------+---------------------------+----+----+---------------------+
```

### Relaciones:
- analysis.document_id        → documents.id
- conversations.user_id       → users.id
- conversations.document_id   → documents.id
- document_chunks.document_id → documents.id
- documents.owner_id          → users.id
- messages.conversation_id    → conversations.id

---

### ✅ Construcción y ejecución

Desde la carpeta del backend (`backendDocAnalyze/`):

#### 🔹 Construir los contenedores:

Para iniciar en una VM GCP: 

```bash
docker-compose -f docker-compose.worker.yml build --no-cache
```
Para iniciar local:

```bash
docker-compose -f docker-compose.yml build --no-cache
```

#### 🔹 Levantar los contenedores:

Para levantar en una VM GCP:

```bash
docker-compose -f docker-compose.worker.yml up -d
```

Para levantar en local:

```bash
docker-compose -f docker-compose.yml up -d
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


### Luejo de levantar contenedores ejecuta la migración de la BD con Alembic (PRIMER USO).

#### Solo para primer uso o instalación:

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
4. Solo si hay actualizaciones sobre el modelo de datos ejecuta el siguiente comando:
    ```bash
    alembic upgrade head
    ```

## 🌐 Accesos

- **Frontend:** http://35.209.28.34/
- **Backend (FastAPI docs):** http://35.209.132.4:8000/docs