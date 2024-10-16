from ..base_interface import IDocumentTextExtractor


class TxtTextExtractor(IDocumentTextExtractor):
    def extract_text(self, file_path: str) -> str:
        if not file_path.endswith('.txt'):
            raise ValueError("Invalid file type. Expected a .txt file.")
        text = ""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
        except Exception as e:
            print(f"Error in TXT extraction: {e}")
        return text
