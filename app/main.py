from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import auth, documents, analysis
from app.core.tasks import celery_app

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

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.on_event("startup")
async def startup_event():
    print("Aplicación iniciada y lista para recibir solicitudes.")

@app.on_event("shutdown")
async def shutdown_event():
    print("Aplicación finalizada correctamente.")
