class QuizParameters:

    @staticmethod
    def get_question_num(context, default=-1):
        # Return the user's question_num, default can be customized
        return context.user_data.get('question_num', default)

    @staticmethod
    def set_question_num(context, new_value):
        if isinstance(new_value, int) and new_value >= 0:
            context.user_data['question_num'] = new_value

    @staticmethod
    def get_question_timer(context, default=0):
        # Return the user's question_timer, default can be customized
        return context.user_data.get('question_timer', default)

    @staticmethod
    def set_question_timer(context, new_value):
        if isinstance(new_value, int) and new_value >= 0:
            context.user_data['question_timer'] = new_value

    @staticmethod
    def get_is_premium(context, default=False):
        # Return if the user is premium, customizable default
        return context.user_data.get('is_premium', default)

    @staticmethod
    def set_is_premium(context, new_value:bool):
        if isinstance(new_value, bool):
            context.user_data['is_premium'] = new_value

    ################################## UPDATE QUIZ MODES ####################################

    @staticmethod
    def get_mode(context, default=None):
        # Return the bot's quiz mode, customizable default
        return context.bot_data.get('mode', default)

        
    @staticmethod
    def is_quiz_mode(context):
        # Check if quiz mode is enabled for the user
        return context.bot_data['mode'] in [
                'premium_quiz', 'formatted_quiz', "sanfoundry_quiz"
        ]

    @staticmethod
    def is_formatted_quiz_mode(context):
        return context.bot_data['mode'] == 'formatted_quiz'
        
    @staticmethod
    def set_formatted_quiz_mode(context):
        # Set the bot's quiz mode to formatted
        context.bot_data['mode'] = 'formatted_quiz'

    @staticmethod
    def is_premium_quiz_mode(context):
        return context.bot_data.get('mode') == 'premium_quiz'

    @staticmethod
    def set_premium_quiz_mode(context):
        # Set the bot's quiz mode to premium
        context.bot_data['mode'] = 'premium_quiz'


    @staticmethod
    def is_sanfoundry_quiz_mode(context):
        return context.bot_data['mode'] == 'sanfoundry_quiz'

    @staticmethod
    def set_sanfoundry_quiz_mode(context):
        # Set the bot's quiz mode to sanfoundry
        context.bot_data['mode'] = 'sanfoundry_quiz'
    
    @staticmethod
    def is_summarize_mode(context):
        return context.bot_data['mode'] == 'summarize'
        
    @staticmethod
    def set_summarize_mode(context):
        # Set bot mode to summarize
        context.bot_data['mode'] = 'summarize'

    @staticmethod
    def set_imagine_mode(context):
        # Set bot mode to imagine
        context.bot_data['mode'] = 'imagine'

    @staticmethod
    def is_imagine_mode(context):
        return context.bot_data['mode'] == 'imagine'

    @staticmethod
    def set_gpt_mode(context):
        # Set bot mode to gpt
        context.bot_data['mode'] = 'gpt'
        
    @staticmethod
    def is_gpt_mode(context):
        return context.bot_data['mode'] == 'gpt'

    @staticmethod
    def remove_mode(context):
        # Remove the bot's quiz mode
        context.bot_data['mode'] = None
