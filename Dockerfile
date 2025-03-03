# Utilizamos una imagen base oficial de Python
FROM python:3.10-slim

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos los archivos necesarios
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el proyecto
COPY . .

# Exponemos el puerto donde correrá FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
