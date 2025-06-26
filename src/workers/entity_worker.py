import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from infrastructure.db.postgres import get_conn
from infrastructure.logger import log_info, log_error
from infrastructure.llm.providers.gateway import LLMGateway
from infrastructure.llm.prompts.entities_extraction import ENTITY_EXTRACTION_PROMPT


ENTITY_EXTRACTION_PROMPT = ENTITY_EXTRACTION_PROMPT

def extract_entities(cv_id: str):
    log_info(f"[EntityWorker] Start entity extraction for CV: {cv_id}")

    # 1. Extract raw_text from cv_texts table
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT raw_text FROM cv_texts WHERE cv_id = %s", (cv_id,))
            row = cur.fetchone()
            if not row or not row[0]:
                log_error(f"[EntityWorker] No raw_text found for cv_id={cv_id}")
                return
            raw_text = row[0]
    except Exception as e:
        log_error(f"[EntityWorker] DB error when fetching raw_text for {cv_id}: {e}")
        return

    # 2. Call LLM to extract entities
    try:
        llm = LLMGateway(provider="gemini")
        entities = llm.extract_entities(ENTITY_EXTRACTION_PROMPT, raw_text)
        log_info(f"[EntityWorker] LLM extraction done for {cv_id}")
    except Exception as e:
        log_error(f"[EntityWorker] LLM extraction failed for {cv_id}: {e}")
        return

    # 3. Save result to cv_entities
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("""
                INSERT INTO cv_entities (cv_id, entities_json)
                VALUES (%s, %s)
                ON CONFLICT (cv_id)
                DO UPDATE SET
                    entities_json = EXCLUDED.entities_json,
                    updated_at = NOW();
            """, (cv_id, entities))
            log_info(f"[EntityWorker] Saved entities for {cv_id}")
    except Exception as e:
        log_error(f"[EntityWorker] DB error when saving entities for {cv_id}: {e}")

# Để worker chạy được với RQ:
# from workers.entity_worker import extract_entities