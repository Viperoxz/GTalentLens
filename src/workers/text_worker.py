# src/workers/text_worker.py
import sys
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from infrastructure.queue.redis_queue import entity_queue
from infrastructure.db.postgres import save_raw_text
from services.text_extractor.pdf import PDFTextExtractor
from infrastructure.logger import log_info, log_error

def extract_and_enqueue_entities(cv_id: str, file_path: str) -> None:
    """Step 1: Extract PDF → save raw_text into DB → push cv_id to entity_queue."""
    log_info(f"[TextWorker] Start extract: {file_path}")

    extractor = PDFTextExtractor()
    result = extractor.extract_text(file_path)

    raw_text = result.get("raw_text")
    if not raw_text:
        log_error(f"[TextWorker] Extraction failed for {cv_id}: {result.get('error')}")
        return

    # 1) Save to PostgreSQL
    try:
        save_raw_text(cv_id=cv_id, file_path=file_path, raw_text=raw_text)
        log_info(f"[TextWorker] Saved raw_text for {cv_id} ({len(raw_text)} chars)")
    except Exception as e:
        log_error(f"[TextWorker] DB error {cv_id}: {e}")
        return

    # 2) Push to Extract Entities (only cv_id)
    entity_queue.enqueue("workers.entity_worker.extract_entities", cv_id)
    log_info(f"[TextWorker] Enqueued {cv_id} → entity_queue")
