# text_parser_manager.py
from .formatted_text_to_mcq import FormattedTextToMCQ
from .general_text_to_mcq import GeneralTextToMCQ
from .sanfoundry_text_to_mcq import SanfoundryTextToMCQ
from bot.modules.quizzes.quizz_parameters import QuizParameters

class TextToMCQ:
    def __init__(self, context):
        # Choose the parser based on the is_premium flag
        if QuizParameters.is_formatted_quiz_mode(context):
            self.parser = FormattedTextToMCQ()
        elif QuizParameters.is_premium_quiz_mode(context):
            self.parser = GeneralTextToMCQ()
        elif QuizParameters.is_sanfoundry_quiz_mode(context):
            self.parser = SanfoundryTextToMCQ()
        
    async def generate_mcq_from_text(self, source: str, text: str, limit: int = -1) -> list:
        # Call the parse_text method of the appropriate parser
        return await self.parser.generate_from_text( source, text, limit)