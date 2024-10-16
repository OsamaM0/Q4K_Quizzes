from ..base_interface import IDocumentTextExtractor
from docx import Document  # python-docx for DOCX files


class DocxExtractor(IDocumentTextExtractor):
    async def extract_text(self, file_path: str) -> str:
        if not file_path.endswith('.docx'):
            raise ValueError("Invalid file type. Expected a .docx file.")
        text = ""
        try:
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            print(f"Error in DOCX extraction: {e}")
        return text
