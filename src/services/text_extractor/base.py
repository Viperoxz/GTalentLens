# src/services/text_extractor/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class TextExtractor(ABC):
    @abstractmethod
    def extract_text(self, file_path: str) -> Dict[str, Any]:
        pass
