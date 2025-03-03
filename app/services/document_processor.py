from typing import Optional
from PyPDF2 import PdfReader
import docx
from io import BytesIO
from fastapi import UploadFile


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
