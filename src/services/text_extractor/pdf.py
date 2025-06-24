# src/services/text_extractor/pdf.py
from typing import Dict, Any
from pathlib import Path
import fitz  # PyMuPDF
import sys

CUR_FILE = Path(__file__).resolve()
ROOT_DIR = CUR_FILE.parents[3]
sys.path.insert(0, str(ROOT_DIR))

from src.services.text_extractor.base import TextExtractor

class PDFTextExtractor(TextExtractor):
    def extract_text(self, file_path: str) -> Dict[str, Any]:
        file_path = str(file_path)
        if not file_path.lower().endswith('.pdf'):
            return {"file_path": file_path, "raw_text": "", "error": "Unsupported file type"}

        try:
            doc = fitz.open(file_path)
            raw_text = "".join([doc.load_page(i).get_text() for i in range(len(doc))])
            doc.close()
            return {"file_path": file_path, "raw_text": raw_text}
        except Exception as e:
            return {"file_path": file_path, "raw_text": "", "error": str(e)}

if __name__ == "__main__":
    file_path = str(ROOT_DIR / "src/dummies_data/yen-nguyen.pdf")

    extractor = PDFTextExtractor()
    result = extractor.extract_text(file_path)

    print("\n====== Kết quả Extract PDF ======")
    print(f"File path: {result.get('file_path')}")
    
    if 'error' in result:
        print(f"❌ Lỗi: {result['error']}")
    else:
        print("✅ Trích xuất thành công:")
        print(f"Full nội dung:\n{result['raw_text']}...")
        print(f"Số ký tự: {len(result['raw_text'])}")