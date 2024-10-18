# # general_text_parser.py
# import modelbit
# from .base_interface import MCQGenerator
#
# class GeneralTextToMCQ(MCQGenerator):
#     def generate_from_text(self, text: str) -> dict:
#         try:
#             data = modelbit.get_inference(
#                 region="us-east-2.aws",
#                 workspace="flashpost",
#                 deployment="mcq_extractor",
#                 data=text
#             )
#             return data["data"]
#         except Exception as e:
#             print(f"Error during inference: {e}")
#             return {}
# general_text_parser.py
import re

from ..g4f import G4F
from .base_interface import MCQGenerator
import time

class GeneralTextToMCQ():
    def __init__(self):
        self._prompt = """Pretend you are a teacher preparing a quiz for the text I will provide. Each quiz question should follow the format below. Ensure that you carefully recheck the questions and answers for accuracy. The output should be a ready-to-use list of dictionaries for the Python eval function:

        [
          {
            "question": "WRITE THE QUESTION HERE",
            "options": ["A) OPTION_1", "B) OPTION_2", "C) OPTION_3", "D) OPTION_4"],
            "answer": INDEX_OF_CORRECT_ANSWER_IN_OPTIONS_LIST,
            "explanation": "EXPLAIN WHY THE ANSWER IS CORRECT"
          },
          {
            ...
          }
        ]
        """

    async def generate_from_text(self, text: str, limit: int) -> list:
        try:
            k = 100
            question_lst = []
            for i in range(100):
                for i in range(0, len(text), k):
                    final_prompt = self._prompt + "text: " + text[i:i+k]
                    data = await G4F.chatgpt(final_prompt)
                    if data:
                        question_lst.extend(self.format_output(self._escape_special_characters(data)))
    
                    if len(question_lst) >= limit > 0:
                        return question_lst

                    time.sleep(3)

        except Exception as e:
            print(f"Error during inference: {e}")
            return []

    def get_prompt(self):
        return self._prompt

    def format_output(self, data):

        # Regex patterns for questions, options, answers, and explanations
        question_pattern = re.compile(r'"question"\s*:\s*"([^"]+)"')
        options_pattern = re.compile(r'"options"\s*:\s*\[([^\]]+)\]')
        answers_pattern = re.compile(r'"answer"\s*:\s*(\d+)')
        explanation_pattern = re.compile(r'"explanation"\s*:\s*"([^"]+)"')

        # Find all matches
        questions = question_pattern.findall(data)
        options = options_pattern.findall(data)
        answers = answers_pattern.findall(data)
        explanations = explanation_pattern.findall(data)

        # Cleaning up options to remove unwanted comments or extra spaces
        def clean_options(opt_str):
            return [opt.strip().strip('/*').replace('"', '') for opt in opt_str.split(',')]

        # Building list of dictionaries
        result = []
        for i in range(len(questions)):
            try:
                result.append({
                    "question": questions[i].replace('"', '')[:300],
                    "options": clean_options(options[i]),
                    "answer": int(answers[i]),
                    "explanation": explanations[i].replace('"', '')
                })
            except:
                pass

        return result

    def _escape_special_characters(self, text: str):
        # List of special characters to escape
        special_chars = ['.', '*', '_', '/', '\\', '-', '+']
    
        # Create a regular expression pattern to match the special characters
        pattern = '[' + re.escape(''.join(special_chars)) + ']'
    
        # Use re.sub() to replace each special character with a backslash followed by the character
        escaped_text = re.sub(pattern, r'\\\g<0>', text)
    
        return escaped_text