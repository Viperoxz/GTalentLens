# src/test_cv_flow.py
import sys
import os
from pathlib import Path
from uuid import uuid4
import time

ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

from orchestrator.orchestrator import handle_cv_upload
from infrastructure.db.postgres import get_conn
from infrastructure.logger import log_info, log_error

def test_cv_processing_flow():
    """Test the CV text extraction and database storage flow."""
    cv_id = str(uuid4())
    file_path = "/app/src/dummies_data/yen-nguyen.pdf"  # ← mount path trong Docker

    if not os.path.exists(file_path):
        log_error(f"❌ File test không tồn tại: {file_path}")
        return

    log_info(f"🚀 Bắt đầu test với CV ID: {cv_id}, File: {file_path}")

    try:
        job_id = handle_cv_upload(cv_id, file_path)
        log_info(f"📤 Đã enqueue job ID: {job_id}")
    except Exception as e:
        log_error(f"❌ Lỗi khi enqueue: {e}")
        return

    log_info("⏳ Chờ worker xử lý...")
    time.sleep(5)

    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT cv_id, file_path, raw_text, status FROM cv_texts WHERE cv_id = %s",
                (cv_id,)
            )
            result = cur.fetchone()
            if result:
                db_cv_id, db_file_path, raw_text, status = result
                log_info(f"✅ DB có entry cho CV ID: {db_cv_id}")
                log_info(f"File path: {db_file_path}")
                log_info(f"Status: {status}")
                log_info(f"Extracted text length: {len(raw_text) if raw_text else 0} chars")
                if status == "text_extracted" and raw_text:
                    log_info("🎉 Test passed: Text được extract và lưu")
                else:
                    log_error("❌ Test failed: Status không đúng hoặc text rỗng")
            else:
                log_error("❌ Test failed: Không tìm thấy entry trong DB")
    except Exception as e:
        log_error(f"❌ Test failed: Lỗi truy vấn DB: {e}")

if __name__ == "__main__":
    test_cv_processing_flow()
