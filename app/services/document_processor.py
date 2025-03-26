from typing import Optional
from PyPDF2 import PdfReader
import docx
from io import BytesIO
from fastapi import UploadFile

import tiktoken
from sentence_transformers import SentenceTransformer
from app.db.crud.document_chunk import create_document_chunk

# ---------------------
# EXTRACCIÓN DE TEXTO
# ---------------------

def extract_text(file: UploadFile) -> Optional[str]:
    ext = file.filename.split(".")[-1].lower()
    
    if ext == "pdf":
        return extract_text_from_pdf(file)
    elif ext == "docx":
        return extract_text_from_docx(file)
    elif ext == "txt":
        return extract_text_from_txt(file)
    else:
        return None

def extract_text_from_pdf(file: UploadFile) -> str:
    reader = PdfReader(BytesIO(file.file.read()))
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def extract_text_from_docx(file: UploadFile) -> str:
    doc = docx.Document(BytesIO(file.file.read()))
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)

def extract_text_from_txt(file: UploadFile) -> str:
    return file.file.read().decode("utf-8")

# ---------------------
# CHUNKING DE TEXTO
# ---------------------

encoding = tiktoken.get_encoding("cl100k_base")

def chunk_text(text: str, max_tokens: int = 500, overlap: int = 50) -> list[str]:
    tokens = encoding.encode(text)
    chunks = []
    start = 0
    while start < len(tokens):
        end = start + max_tokens
        chunk = tokens[start:end]
        chunks.append(encoding.decode(chunk))
        start += max_tokens - overlap
    return chunks

# ---------------------
# EMBEDDINGS + ALMACENAMIENTO
# ---------------------

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text: str) -> list[float]:
    embedding = embedding_model.encode(text, convert_to_numpy=True)
    return embedding.tolist()

def process_and_store_chunks_sqlalchemy(db, document_id: int, full_text: str):
    chunks = chunk_text(full_text)

    for index, chunk in enumerate(chunks):
        embedding = generate_embedding(chunk)
        create_document_chunk(
            db=db,
            document_id=document_id,
            chunk_text=chunk,
            embedding=embedding,
            chunk_index=index
        )

    db.commit()

