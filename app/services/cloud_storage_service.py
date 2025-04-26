from google.cloud import storage
from fastapi import UploadFile
from tempfile import NamedTemporaryFile

def upload_file_to_gcs(bucket_name: str, upload_file: UploadFile, destination_blob_name: str):
    """Sube un archivo de FastAPI UploadFile a Google Cloud Storage"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Guardar temporalmente el archivo en el sistema
    with NamedTemporaryFile(delete=True) as temp_file:
        contents = upload_file.file.read()
        temp_file.write(contents)
        temp_file.flush()
        blob.upload_from_filename(temp_file.name)

def download_file_from_gcs(bucket_name: str, blob_name: str, destination_file_name: str):
    """Descarga un archivo de GCS a un archivo local temporal"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.download_to_filename(destination_file_name)
