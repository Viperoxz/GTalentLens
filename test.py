import sys
from pathlib import Path
import uuid
import os
import time

# Thêm src vào sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from src.orchestrator.orchestrator import handle_cv_upload

test_file_path = "src/dummies_data/yen-nguyen.pdf"

if not os.path.exists(test_file_path):
    print(f"❌ Không tìm thấy file test: {test_file_path}")
    sys.exit(1)

test_cv_id = str(uuid.uuid4())
print(f"🚀 Enqueue extract_text cho CV: {test_cv_id}")

job_id = handle_cv_upload(test_cv_id, test_file_path)
print(f"✅ Đã enqueue job (job_id={job_id})")

print("\n👉 Để worker xử lý job, hãy chạy lệnh sau ở terminal khác:")
print("   python3 -m workers.text_worker")

print("\n⏳ Đợi 5 giây cho worker xử lý (hoặc kiểm tra log/DB)...")
time.sleep(5)

print("\n🎯 Kiểm tra kết quả trong bảng 'cv_texts' của Postgres hoặc file log trong thư mục logs/")
print("   Ví dụ: SELECT * FROM cv_texts WHERE cv_id = '%s';" % test_cv_id)