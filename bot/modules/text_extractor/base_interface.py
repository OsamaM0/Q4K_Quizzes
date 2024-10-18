from abc import ABC, abstractmethod


# Interface for document processing
class IDocumentTextExtractor(ABC):
    @abstractmethod
    async def extract_text(self, path: str) -> str:
        pass
