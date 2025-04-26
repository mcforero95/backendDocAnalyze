# 📄 Backend y Frontend de Análisis de Documentos con LLM

Proyecto para análisis, resumen y consulta de documentos utilizando FastAPI, recuperación de contexto (RAG), Gemini IA y PostgreSQL, desplegado sobre GCP de forma escalable.

---

## 🚀 Tecnologías utilizadas

- **Backend:** Python 3.10, FastAPI, PostgreSQL (Cloud SQL), Alembic
- **LLM:** Gemini IA de Google vía API Flash 2.0
- **Embeddings locales:** Sentence Transformers (`all-MiniLM-L6-v2`)
- **Mensajería:** Google Cloud Pub/Sub
- **Almacenamiento de documentos:** Google Cloud Storage
- **Orquestación:** Docker
- **Despliegue:** GCP (Compute Engine + Load Balancer + Autoscaling)

---

## 🛠️ Instalación y ejecución local

### ✅ Requisitos previos

- Docker y Docker Compose
- Clave de API de Google para Gemini IA
- Variables de entorno configuradas
- IP pública de tu instancia de Cloud SQL (Base de Datos PostgreSQL en GCP).

### ✅ Variables de entorno

```env
# Base de datos PostgreSQL (Cloud SQL)
DATABASE_URL=postgresql://postgres:analyzedb@<IP CLOUD SQL>:5432/analyze_db
POSTGRES_DB=analyze_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=analyzedb
POSTGRES_HOST=<IP CLOUD SQL>
POSTGRES_PORT=5432

# Seguridad JWT
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Ruta del modelo de lenguaje
GEMINI_API_KEY=<Tu API Key de Gemini>
GEMINI_MODEL_NAME=gemini-2.0-flash

# Redis (para cachear datos)
REDIS_URL=redis://redis:6379/0

# Configuración de GCP
GCP_PROJECT_ID=<ID Proyecto GCP>
CLOUD_STORAGE_BUCKET=doc-analyze-uploads
PUBSUB_TOPIC=doc-process-topic
PUBSUB_SUBSCRIPTION=doc-process-subscription
```

---

## 🧠 Funcionalidades clave

- ✅ Subida de documentos (`.pdf`, `.docx`, `.txt`) a **Cloud Storage**.
- ✅ Procesamiento de documentos de forma asíncrona usando **Pub/Sub** y **Workers**.
- ✅ Extracción y segmentación del texto en *chunks*.
- ✅ Generación de **embeddings** por chunk.
- ✅ Resumen automático del documento usando **Gemini IA**.
- ✅ Chat de preguntas y respuestas sobre el contenido.
- ✅ **Recuperación de contexto (RAG)** usando los chunks relevantes.
- ✅ Historial de conversaciones por usuario.
- ✅ Escalabilidad automática en GCP con **Autoscaling** y **Load Balancer**.

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

## ✅ Construcción y ejecución

Desde la carpeta del backend (`backendDocAnalyze/`):

#### 🔹 Construir contenedores:

```bash
docker-compose build --no-cache
```

#### 🔹 Levantar contenedores:

```bash
docker-compose up -d
```

#### 🔹 Ver logs del backend:

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

---

### 🗄️ Migraciones de base de datos (Primer uso o cambios de modelos)

1. Accede al contenedor backend:
    ```bash
    docker exec -it backend_doc_analyze bash
    ```

2. Crea carpeta de migraciones (si no existe):
    ```bash
    mkdir -p /app/alembic/versions
    ```

3. Genera la migración inicial:
    ```bash
    alembic revision --autogenerate -m "Initial migration"
    alembic upgrade head
    ```

4. Posteriormente, solo ejecutar cuando haya cambios en el modelo de datos:
    ```bash
    alembic upgrade head
    ```

---

## 🌐 Accesos

- **Frontend:** http://<IP Frontend>/
- **Backend (FastAPI docs):** http://<IP Backend>:8000/docs

---

# ⚡️ Notas importantes

- Los archivos **no se almacenan en disco local**. Todo se guarda en **Cloud Storage**.
- El procesamiento de documentos es **asíncrono** y distribuido entre múltiples **Workers**.
- La base de datos ahora es **Cloud SQL** en GCP, no local.
- El sistema es escalable a cientos o miles de usuarios gracias a **Autoscaling** de GCP.

---
