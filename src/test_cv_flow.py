# src/test_cv_flow.py
import sys
import os
from pathlib import Path
from uuid import uuid4
import time

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

from orchestrator.orchestrator import handle_cv_upload
from infrastructure.db.postgres import get_conn
from infrastructure.logger import log_info, log_error

def test_cv_processing_flow():
    """Test the CV text extraction and database storage flow."""
    # Sample input
    cv_id = str(uuid4())  # Generate unique CV ID
    # file_path = str(ROOT_DIR / "dummies_data/yen-nguyen.pdf")
    file_path = "/root/nam/src/dummies_data/yen-nguyen.pdf"

    # Verify file exists
    if not os.path.exists(file_path):
        log_error(f"Test file not found: {file_path}")
        return

    log_info(f"Starting test for CV ID: {cv_id}, File: {file_path}")

    # Step 1: Trigger CV upload (enqueue to cv_queue)
    try:
        job_id = handle_cv_upload(cv_id, file_path)
        log_info(f"Enqueued job ID: {job_id}")
    except Exception as e:
        log_error(f"Failed to enqueue CV upload: {e}")
        return

    # Step 2: Wait for job to complete (simulating RQ worker processing)
    log_info("Waiting for job to complete...")
    time.sleep(5)  # Adjust based on processing time

    # Step 3: Verify database entry
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT cv_id, file_path, raw_text, status FROM cv_texts WHERE cv_id = %s",
                (cv_id,)
            )
            result = cur.fetchone()
            if result:
                db_cv_id, db_file_path, raw_text, status = result
                log_info(f"Database entry found for CV ID: {db_cv_id}")
                log_info(f"File path: {db_file_path}")
                log_info(f"Status: {status}")
                log_info(f"Extracted text length: {len(raw_text) if raw_text else 0} characters")
                if status == "text_extracted" and raw_text:
                    log_info("✅ Test passed: Text extracted and saved to database")
                else:
                    log_error("❌ Test failed: Unexpected status or empty text")
            else:
                log_error("❌ Test failed: No database entry found")
    except Exception as e:
        log_error(f"❌ Test failed: Database query error: {e}")

if __name__ == "__main__":
    test_cv_processing_flow()