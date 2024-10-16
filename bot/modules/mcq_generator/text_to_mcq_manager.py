# text_parser_manager.py
from .formatted_text_to_mcq import FormattedTextToMCQ
from .general_text_to_mcq import GeneralTextToMCQ


class TextToMCQ:
    def __init__(self, is_premium: bool):
        # Choose the parser based on the is_premium flag
        self.parser = GeneralTextToMCQ() if is_premium else FormattedTextToMCQ()

    async def generate_mcq_from_text(self, text: str, limit: int = 0) -> list:
        # Call the parse_text method of the appropriate parser
        return self.parser.generate_from_text(text, limit)