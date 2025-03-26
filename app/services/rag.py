import numpy as np
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session
from app.db.models.document_chunk import DocumentChunk

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_most_relevant_chunks(db: Session, document_id: int, question: str, top_k: int = 3) -> list[str]:
    # Generar embedding de la pregunta
    question_embedding = embedding_model.encode(question, convert_to_numpy=True)

    # Obtener los chunks del documento
    chunks = db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).all()

    # Calcular similitud coseno entre pregunta y cada chunk
    scored_chunks = []
    for chunk in chunks:
        chunk_embedding = np.array(chunk.embedding)
        score = cosine_similarity(question_embedding, chunk_embedding)
        scored_chunks.append((score, chunk.chunk_text))

    # Ordenar por similitud y devolver top_k chunks
    scored_chunks.sort(reverse=True, key=lambda x: x[0])
    top_chunks = [text for _, text in scored_chunks[:top_k]]
    return top_chunks

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
