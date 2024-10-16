from web_extractor.html_extractor import HTMLExtractor
from file_extractor import PdfExtractor, DocxExtractor, TxtTextExtractor, PptxTextExtractor
from audio_extractor.audio_extractor import AudioExtractor


class TextExtractor:
    def __init__(self):
        # Initialize different processors
        self.web_processor = HTMLExtractor()
        self.pdf_processor = PdfExtractor()
        self.docx_processor = DocxExtractor()
        self.txt_processor = TxtTextExtractor()
        self.pptx_processor = PptxTextExtractor()
        self.audio_processor = AudioExtractor()
        self.history = []  # To keep track of processed documents

    async def extract_text_from_document(self, path: str, save_history: bool = False) -> str:
        # Determine the type of document based on the input and use the right processor
        processor = await self._choose_processor(path)
        if not processor:
            return "Unsupported document type or invalid input."

        # Extract the text using the chosen processor
        result = await processor.extract_text(path)
        if save_history:
            await self._save_history(path, result)
        return result

    async def _choose_processor(self, path: str):
        # Determine the processor based on the file extension or URL format
        if path.startswith("http://") or path.startswith("https://"):
            return self.web_processor
        elif path.endswith(".pdf"):
            return self.pdf_processor
        elif path.endswith(".docx"):
            return self.docx_processor
        elif path.endswith(".txt"):
            return self.txt_processor
        elif path.endswith(".pptx"):
            return self.pptx_processor
        elif path.endswith(('.wav', '.flac', '.mp3', '.m4a')):
            return self.audio_processor
        else:
            return None

    async def _save_history(self, path: str, result: str) -> None:
        self.history.append({"path": path, "result": result})

    async def get_history(self) -> list:
        return self.history
