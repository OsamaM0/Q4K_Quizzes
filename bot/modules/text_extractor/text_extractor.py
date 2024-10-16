from .file_extractor.pdf_extractor import PdfExtractor
from .file_extractor.docx_extractor import DocxExtractor
from .file_extractor.txt_extractor import TxtTextExtractor
from .file_extractor.pptx_extractor import PptxTextExtractor
from .audio_extractor.audio_extractor import AudioExtractor
from .web_extractor.html_extractor import HTMLExtractor
import re


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

    def extract_text_from_document(self, path: str, save_history: bool = False) -> str:
        # Determine the type of document based on the input and use the right processor
        processor = self._choose_processor(path)
        if not processor:
            return "Unsupported document type or invalid input."

        # Extract the text using the chosen processor
        result = self._escape_special_characters(processor.extract_text(path))
        if save_history:
            self._save_history(path, result)

        return result

    def _choose_processor(self, path: str):
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

    def _save_history(self, path: str, result: str) -> None:
        self.history.append({"path": path, "result": result})

    def get_history(self) -> list:
        return self.history

    def _escape_special_characters(self, text: str):
        # List of special characters to escape
        special_chars = ['.', '*', '_', '/', '\\', '-', '+']

        # Create a regular expression pattern to match the special characters
        pattern = '[' + re.escape(''.join(special_chars)) + ']'

        # Use re.sub() to replace each special character with a backslash followed by the character
        escaped_text = re.sub(pattern, r'\\\g<0>', text)

        return escaped_text
