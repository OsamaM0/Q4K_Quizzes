from ..base_interface import IDocumentTextExtractor
import fitz  # PyMuPDF for PDFs


class PdfExtractor(IDocumentTextExtractor):
    def extract_text(self, file_path: str) -> str:
        if not file_path.endswith('.pdf'):
            raise ValueError("Invalid file type. Expected a .pdf file.")
        text = ""
        try:
            with fitz.open(file_path) as doc:
                for page in doc:
                    text += page.get_text()
        except Exception as e:
            print(f"Error in PDF extraction: {e}")
        return text
