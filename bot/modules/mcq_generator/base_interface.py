from abc import ABC, abstractmethod

class MCQGenerator(ABC):
    @abstractmethod
    def generate_from_text(self, text: str, limit: int) -> dict:
        """Parse the input text and return a dictionary."""
        pass