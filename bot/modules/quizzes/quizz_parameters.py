class QuizParameters:
    _question_num = 1       # Private class variable for question number
    _question_timer = 30    # Private class variable for timer (in seconds)
    _is_quiz = False

    @staticmethod
    def get_question_num():
        return QuizParameters._question_num

    @staticmethod
    def set_question_num(new_value):
        QuizParameters._question_num = new_value

    @staticmethod
    def get_question_timer():
        return QuizParameters._question_timer

    @staticmethod
    def set_question_timer(new_value):
        QuizParameters._question_timer = new_value

    @staticmethod
    def get_is_quiz():
        return QuizParameters._question_timer

    @staticmethod
    def set_is_quiz(new_value):
        QuizParameters._is_quiz = new_value