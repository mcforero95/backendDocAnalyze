from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import auth, documents, analysis, conversations
from app.core.config import settings
from app.services.cloud_storage_service import upload_file_to_gcs_from_pubsub
from google.cloud import pubsub_v1
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
        upload_file_to_gcs_from_pubsub(data)
        message.ack()
    except Exception as e:
        print(f"Error subiendo a GCS desde mensaje Pub/Sub: {e}")
        message.nack()

async def start_pubsub_listener():
    global subscriber, streaming_pull_future
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(settings.GCP_PROJECT_ID, settings.PUBSUB_SUBSCRIPTION)
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Escuchando mensajes en {subscription_path}...")
    await asyncio.get_event_loop().run_in_executor(None, streaming_pull_future.result)

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
