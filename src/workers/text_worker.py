# src/workers/text_worker.py
from services.text_extractor.pdf import PDFTextExtractor
from qdrant_client import QdrantClient
from qdrant_client.http import models
from infrastructure.queue.redis_queue import entity_queue

def extract_and_enqueue_entities(cv_id: str, file_path: str):
    extractor = PDFTextExtractor()
    result = extractor.extract_text(file_path)

    raw_text = result.get("raw_text")
    if not raw_text:
        print(f"[Worker] Extraction failed: {result.get('error')}")
        return

    # Save to Qdrant
    qdrant = QdrantClient(host="qdrant", port=6333)
    qdrant.upsert(
        collection_name="cv_raw_texts",
        points=[models.PointStruct(
            id=hash(file_path),
            vector=None,
            payload={"cv_id": cv_id, "file_path": file_path, "raw_text": raw_text}
        )]
    )

    # Push to next step
    entity_queue.enqueue("workers.entity_worker.extract_entities", cv_id, raw_text)
    print(f"[Worker] Pushed to entity queue: {cv_id}")
