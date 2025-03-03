from celery import Celery
from app.core.config import settings

REDIS_URL = settings.REDIS_URL

celery_app = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

@celery_app.task
def process_document_task(document_text: str):
    from app.services.summarizer import summarize_text
    return summarize_text(document_text)
