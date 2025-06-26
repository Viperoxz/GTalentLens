# src/orchestrator/orchestrator.py
from infrastructure.queue.redis_queue import cv_queue
from workers.text_worker import extract_and_enqueue_entities

def handle_cv_upload(cv_id: str, file_path: str):
    job = cv_queue.enqueue(extract_and_enqueue_entities, cv_id, file_path)
    return job.id
