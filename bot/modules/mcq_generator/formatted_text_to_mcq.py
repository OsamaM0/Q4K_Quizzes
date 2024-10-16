# formatted_text_parser.py
import re
from .base_interface import MCQGenerator

class FormattedTextToMCQ(MCQGenerator):
    def generate_from_text(self, text: str, limit: int) -> dict:
        questions = []
        try:
            lines = text.split('\n')
            question_pattern = r'^\d+\. .+|^\d+\- .+|(What|Why|How|When|Where|Who|Which)\s'
            option_pattern = r'^\s*[A-Da-d][\-\.\)] .+'
            answer_pattern = r'(Answer: [A-Da-d]|ANSWER:[A-Da-d]|ans: [A-Da-d]|Answer [A-Da-d]|ANSWER [A-Da-d]|ans [A-Da-d])'
            explination_pattern = r'(Explanation:[A-Da-d]|Explanation[A-Da-d]|Explanation :[A-Da-d]|Explanation :[A-Da-d]|Explanation: [A-Da-d]|Explanation : [A-Da-d])'
            k = {"a": 0, "b": 1, "c": 2, "d": 3, "A": 0, "B": 1, "C": 2, "D": 3}

            question = None
            for line in lines:
                line = line.strip()

                if line and not line.startswith("Explanation:") and not line.startswith("Hint:"):
                    if re.match(question_pattern, line):
                        if question:
                            questions.append(question)
                        question = {
                            "question": line,
                            "options": [],
                            "answer": "",
                            "explanation": "No Explanation",
                            "long_question": [],
                            "images": []
                        }

                    elif re.match(option_pattern, line):
                        if question:
                            if re.match(answer_pattern, line):
                                question["answer"] = k[re.findall(answer_pattern, line)[0][-1]]
                            option = re.sub(r'^\s*[A-Da-d][\-\.\)]\s*', '', line)
                            question["options"].append(option)

                    elif re.match(answer_pattern, line):
                        if question:
                            question["answer"] = k[re.findall(answer_pattern, line)[0][-1]]

                    elif re.match(explination_pattern, line):
                        if question:
                            question["explanation"] = line

                    elif question:
                        question["question"] += " " + line

            if question:
                questions.append(question)

            if len(questions) >= limit > 0:
                return questions

        except Exception as e:
            print(f"Error parsing questions: {e}")

        return questions
