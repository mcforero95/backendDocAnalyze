from google.cloud import pubsub_v1
import json
from app.core.config import settings

def publish_to_pubsub(topic_name: str, data: dict):
    """Publica un mensaje JSON en un topic de Pub/Sub"""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(settings.GCP_PROJECT_ID, topic_name)
    message_json = json.dumps(data)
    message_bytes = message_json.encode("utf-8")
    future = publisher.publish(topic_path, message_bytes)
    return future.result()
