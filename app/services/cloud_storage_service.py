from google.cloud import storage
import base64

def upload_file_to_gcs_from_pubsub(data: dict):
    from google.cloud import storage

    bucket_name = data["bucket_name"]
    file_content = base64.b64decode(data["file_content"])
    destination_blob_name = data["blob_name"]

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(file_content)
    print(f"Archivo subido: {destination_blob_name}")

def download_file_from_gcs(bucket_name: str, blob_name: str, destination_file_name: str):
    """Descarga un archivo de GCS a un archivo local temporal"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.download_to_filename(destination_file_name)
