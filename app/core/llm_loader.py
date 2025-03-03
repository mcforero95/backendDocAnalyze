from llama_cpp import Llama
from app.core.config import settings

LLM_MODEL_PATH = settings.LLM_MODEL_PATH

llm = Llama(
    model_path=LLM_MODEL_PATH,
    n_ctx=4096,  # Aumentamos el contexto si el modelo lo soporta
    temperature=0.2,  # Controla la creatividad
    top_p=0.8,  # Controla la diversidad
)

def generate_response(prompt: str) -> str:
    result = llm(
        prompt,
        max_tokens=1024,  # Más tokens para respuestas más largas
        stop=["\n\n", "<|endoftext|>"],  # Opcional, para cortar bien la respuesta
    )
    return result["choices"][0]["text"].strip()
