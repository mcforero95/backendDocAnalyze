from app.core.llm_loader import generate_response

def summarize_text(text: str) -> str:
    prompt = (
        "Resume el siguiente texto de forma clara y concisa:\n\n"
        f"{text}\n\n"
        "Resumen:"
    )
    return generate_response(prompt)
