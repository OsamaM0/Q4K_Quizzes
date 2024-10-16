class QuizParameters:

    @staticmethod
    def get_question_num(context):
        # Return the user's question_num, default to 0
        return context.user_data.get('question_num', 0)

    @staticmethod
    def set_question_num(context, new_value):
        # Set the question_num for the current user
        context.user_data['question_num'] = new_value

    @staticmethod
    def get_question_timer(context):
        # Return the user's question_timer, default to 0 (Unlimited time)
        return context.user_data.get('question_timer', 0)

    @staticmethod
    def set_question_timer(context, new_value):
        # Set the question_timer for the current user
        context.user_data['question_timer'] = new_value

    @staticmethod
    def get_is_quiz(context):
        # Return if the quiz mode is enabled for the user, default to False
        return context.user_data.get('is_quiz', False)

    @staticmethod
    def set_is_quiz(context, new_value):
        # Set whether quiz mode is enabled for the current user
        context.user_data['is_quiz'] = new_value

    @staticmethod
    def get_is_premium(context):
        # Return if the user is premium, default to False
        return context.user_data.get('is_premium', False)

    @staticmethod
    def set_is_premium(context, new_value):
        # Set the premium status for the current user
        context.user_data['is_premium'] = new_value
