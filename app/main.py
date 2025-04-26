from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import auth, documents, analysis, conversations
from app.core.config import settings
from app.services.cloud_storage_service import download_file_from_gcs
from app.services.document_processor import extract_text, process_and_store_chunks_sqlalchemy
from app.db.session import get_db
from google.cloud import pubsub_v1
from sqlalchemy.orm import Session
from tempfile import NamedTemporaryFile
import asyncio
import json

app = FastAPI(
    title="API de análisis de documentos",
    description="API para gestión, análisis y resumen automatizado de documentos con LLM local.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["documents"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["analysis"])
app.include_router(conversations.router, prefix="/api/v1/conversations", tags=["conversations"])

subscriber = None
streaming_pull_future = None

def callback(message):
    try:
        data = json.loads(message.data.decode("utf-8"))
        user_id = data["user_id"]
        document_id = data["document_id"]
        bucket_name = data["bucket_name"]
        blob_name = data["blob_name"]

        print(f"Procesando documento {document_id} del usuario {user_id}")

        # 1. Descargar archivo temporalmente
        with NamedTemporaryFile(delete=True) as temp_file:
            download_file_from_gcs(
                bucket_name=bucket_name,
                blob_name=blob_name,
                destination_file_name=temp_file.name
            )

            # 2. Extraer texto
            class TempUploadFile:
                def __init__(self, filename, filepath):
                    self.filename = filename
                    self.file = open(filepath, "rb")

            temp_upload = TempUploadFile(blob_name, temp_file.name)
            text = extract_text(temp_upload)
            temp_upload.file.close()

        # 3. Procesar y almacenar chunks
        db: Session = next(get_db())
        process_and_store_chunks_sqlalchemy(
            db=db,
            document_id=document_id,
            full_text=text
        )

        print(f"Documento {document_id} procesado exitosamente.")
        message.ack()

    except Exception as e:
        print(f"Error procesando mensaje: {e}")
        message.nack()

async def start_pubsub_listener():
    global subscriber, streaming_pull_future
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(settings.GCP_PROJECT_ID, settings.PUBSUB_SUBSCRIPTION)
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Escuchando mensajes en {subscription_path}...")
    await streaming_pull_future

@app.on_event("startup")
async def startup_event():
    print("Aplicación iniciada y lista para recibir solicitudes.")
    asyncio.create_task(start_pubsub_listener())

@app.on_event("shutdown")
async def shutdown_event():
    print("Aplicación finalizada correctamente.")
    if streaming_pull_future:
        streaming_pull_future.cancel()
    if subscriber:
        subscriber.close()

@app.get("/health")
def health_check():
    return {"status": "ok"}
