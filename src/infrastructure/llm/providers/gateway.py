from .gemini import GeminiLLM

class LLMGateway:
    def __init__(self, provider: str = "gemini", api_key: str = None):
        if provider == "gemini":
            self.llm = GeminiLLM(api_key)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
        
    def extract_entities(self, prompt: str, text: str) -> dict:
        """
        Extract entities from text using the configured LLM provider.
        :param prompt: Prompt guiding the LLM.
        :param text: Input text (raw_text).
        :return: dict of extracted entities.
        """
        return self.llm.extract_entities(prompt, text)