# src/workers/text_jobs.py

from src.services.text_extractor.pdf import PDFTextExtractor

def extract_pdf_job(file_path: str) -> dict:
    print(f"[JOB] 📄 Starting to extract: {file_path}")
    extractor = PDFTextExtractor()
    result = extractor.extract_text(file_path)
    print(f"[JOB] ✅ Finish extraction: {file_path}")
    return result
