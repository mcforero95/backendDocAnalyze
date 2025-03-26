from app.core.llm_loader import generate_response

def answer_question(text: str, question: str) -> str:
    prompt = (
        "Responde con precisión y de forma breve según el siguiente texto extraído de un documento.\n\n"
        f"TEXTO DEL DOCUMENTO:\n{text}\n\n"
        f"PREGUNTA: {question}\n\n"
        "RESPUESTA:"
    )
    return generate_response(prompt)

def answer_question_with_context(context_chunks: list[str], question: str) -> str:
    context = "\n\n".join(context_chunks)
    prompt = (
        "Responde con precisión utilizando el siguiente contexto recuperado del documento:\n\n"
        f"{context}\n\n"
        f"PREGUNTA: {question}\n\n"
        "RESPUESTA:"
    )
    return generate_response(prompt)

