from abc import ABC, abstractmethod

class BaseLLM(ABC):
    @abstractmethod
    def extract_entities(self, prompt: str, text: str) -> dict:
        """
        Extract entities from text using LLM.
        :param prompt: Prompt guiding the LLM.
        :param text: Input text (raw_text).
        :return: dict of extracted entities.
        """
        pass