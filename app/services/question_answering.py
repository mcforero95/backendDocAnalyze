from app.core.llm_loader import generate_response

from app.core.llm_loader import generate_response

def answer_question(text: str, question: str) -> str:
    prompt = (
        "Responde con precisión y de forma breve según el siguiente texto extraído de un documento.\n\n"
        f"TEXTO DEL DOCUMENTO:\n{text}\n\n"
        f"PREGUNTA: {question}\n\n"
        "RESPUESTA:"
    )
    return generate_response(prompt)
