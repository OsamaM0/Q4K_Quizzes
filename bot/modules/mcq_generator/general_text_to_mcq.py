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

from ..ai.ai_modules import AIModules 
from .base_interface import MCQGenerator
import time
from random import shuffle, randint
from bot.modules.quizzes.quiz_database import QuizDataHandler
from langdetect import detect


class GeneralTextToMCQ():
   
    async def generate_from_text(self, source: str, text: str, limit: int, chunk_size: int = 3000) -> list:
        # try:
            quiz_data_handler = QuizDataHandler()
            question_lst = []
            if len(text) < 10:
                return question_lst

            chunks_dict = {}
            # Break the text into manageable chunks
            chunks = [[i,i + chunk_size] for i in range(0, len(text), chunk_size)]
            shuffle(chunks)
            # Iterate over chunks and generate quiz questions for each chunk
            for chunk in chunks:
                chunk_name = f"{chunk[0]}:{chunk[1]}"
                db_question = await quiz_data_handler.get_questions(source, text)
                db_question = db_question.get(chunk_name, None)
                if db_question:
                    # Get questios form database
                    question_lst.extend(db_question)
                    
                else:
                    # Get questions from AI
                    data = await AIModules().generate_quiz(text[chunk[0] : chunk[1]])  # Process each chunk
                    
                    if data:
                        chunks_dict[chunk_name] = self.format_output(self._escape_special_characters(data))
                        # Format and add generated questions to the question list
                        question_lst.extend(chunks_dict[chunk_name])
    
                # Check if the limit is reached
                if len(question_lst) >= limit >= 0:
                    await quiz_data_handler.add_entry(source, text, chunks=chunks_dict)
                    return question_lst[:limit]
                
            await quiz_data_handler.add_entry(source, text, chunks=chunks_dict)
            return question_lst  # Return after all chunks are processed

        # except Exception as e:
        #     print(f"Error during inference: {e}")
        #     return []

    def format_output(self, data):
        # Regex patterns for questions, options, answers, and explanations in both Arabic and English
        question_pattern = re.compile(r'"(?:question|السؤال)"\s*:\s*"([^"]+)"')
        options_pattern = re.compile(r'"(?:options|الخيارات)"\s*:\s*\[([^\]]+)\]')
        answers_pattern = re.compile(r'"(?:answer|الإجابة)"\s*:\s*(\d+)')
        explanation_pattern = re.compile(r'"(?:explanation|التفسير)"\s*:\s*"([^"]+)"')

        # Find all matches
        questions = question_pattern.findall(data)
        options = options_pattern.findall(data)
        answers = answers_pattern.findall(data)
        explanations = explanation_pattern.findall(data)

        def clean_options(opt_str):
            # Remove comments, slashes, backslashes, dots, and extra spaces
            cleaned = re.sub(r'[/*\\"./]', '', opt_str)  # Remove all unwanted characters
            return [opt.strip() for opt in cleaned.split(',') if opt.strip()]  # Clean up extra spaces, ignore empty options

        # Building list of dictionaries
        result = []
        for i in range(len(questions)):
            try:
                result.append({
                    "question": questions[i].replace('"', ''),
                    "options": clean_options(options[i]),
                    "answer": int(answers[i]),
                    "explanation": explanations[i].replace('"', '')
                })
            except:
                pass

        return result


    def _detect_language(self, text):
        """Detects the language of the input text."""
        return detect(text)
            
    def _escape_special_characters(self, text: str):
        # List of special characters to escape
        special_chars = ['.', '*', '_', '-', '+']
    
        # Create a regular expression pattern to match the special characters
        pattern = '[' + re.escape(''.join(special_chars)) + ']'
    
        # Use re.sub() to replace each special character with a backslash followed by the character
        escaped_text = re.sub(pattern, r'\\\g<0>', text)
    
        return escaped_text