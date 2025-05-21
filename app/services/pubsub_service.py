from google.cloud import pubsub_v1
import json
from app.core.config import settings

def publish_to_pubsub(topic_name: str, data: dict):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(settings.GCP_PROJECT_ID, topic_name)

    message_data = json.dumps(data).encode("utf-8")
    future = publisher.publish(topic_path, message_data)
    print(f"Mensaje publicado a {topic_path}")
    return future.result()
