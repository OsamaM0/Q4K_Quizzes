from abc import ABC, abstractmethod

class MCQGenerator(ABC):
    @abstractmethod
    def generate_from_text(self, link_path: str, text: str, limit: int) -> dict:
        """Parse the input text and return a dictionary."""
        pass