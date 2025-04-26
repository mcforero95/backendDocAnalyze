from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.crud.document import get_documents_by_user
from app.db.crud.user import get_user_by_email
from app.core.security import decode_access_token
from app.services.summarizer import summarize_text
from app.services.question_answering import answer_question
from fastapi.security import OAuth2PasswordBearer
from app.db.crud.conversation import create_conversation, add_message
from app.db.models.conversation import Conversation  # Asegúrate de importar Conversation
from app.db.crud.document_chunk import get_chunks_by_document
import logging
import asyncio
from fastapi import HTTPException
from starlette.concurrency import run_in_threadpool

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter()

async def safe_llm_process(func, *args, timeout_seconds=180, **kwargs):
    try:
        return await asyncio.wait_for(
            run_in_threadpool(func, *args, **kwargs),
            timeout=timeout_seconds
        )
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail=f"Tiempo de procesamiento del modelo excedido ({timeout_seconds} segundos)"
        )

@router.get("/summarize/{document_id}")
async def summarize(document_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    user_email = payload.get("sub")
    user = get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no autenticado")
    
    documents = get_documents_by_user(db, user.id)
    document = next((doc for doc in documents if doc.id == document_id), None)
    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    # 🧠 Recuperar todos los chunks del documento
    chunks = get_chunks_by_document(db, document_id)
    chunk_texts = [chunk.chunk_text for chunk in chunks if chunk.chunk_text and chunk.chunk_text.strip()]
    full_text = "\n".join(chunk_texts)

    if not full_text.strip():
        return {"summary": "No hay texto para resumir."}

    # ⚙️ Generar resumen usando Gemini
    summary = await safe_llm_process(summarize_text, full_text)

    # 💬 Verificar si ya existe una conversación
    conversation = db.query(Conversation).filter_by(user_id=user.id, document_id=document_id).first()
    if not conversation:
        conversation = create_conversation(db, user.id, document_id)
        logger.info(f"Conversación creada con ID: {conversation.id}")

    # 🧠 Almacenar resumen como mensaje
    add_message(
        db=db,
        conversation_id=conversation.id,
        question="Resumen del documento",
        answer=summary
    )

    return {"summary": summary}



from app.services.rag import get_most_relevant_chunks
from app.services.question_answering import answer_question, answer_question_with_context

@router.post("/ask/{document_id}")
async def ask(
    document_id: int,
    question: str,
    rag: bool = False,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(token)
    user_email = payload.get("sub")
    user = get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no autenticado")

    documents = get_documents_by_user(db, user.id)
    document = next((doc for doc in documents if doc.id == document_id), None)
    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    conversation = db.query(Conversation).filter_by(user_id=user.id, document_id=document_id).first()
    if not conversation:
        conversation = create_conversation(db, user.id, document_id)
        logger.info(f"Conversación creada con ID: {conversation.id}")

    if rag:
        # Recuperar chunks relevantes y generar respuesta con contexto
        chunks = get_most_relevant_chunks(db, document_id, question, top_k=3)
        answer = await safe_llm_process(answer_question_with_context, chunks, question)
    else:
        # Usar el texto completo del documento como contexto
        answer = await safe_llm_process(answer_question, document.content, question)

    add_message(db, conversation.id, question, answer)
    return {"answer": answer}
