# src/workers/text_jobs.py

from src.services.text_extractor.pdf import PDFTextExtractor

def extract_pdf_job(file_path: str) -> dict:
    print(f"[JOB] 📄 Bắt đầu trích xuất: {file_path}")
    extractor = PDFTextExtractor()
    result = extractor.extract_text(file_path)
    print(f"[JOB] ✅ Trích xuất xong: {file_path}")
    return result
