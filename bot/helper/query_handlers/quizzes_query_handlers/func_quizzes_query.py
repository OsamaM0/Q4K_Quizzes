from telegram import Update
from telegram.ext import ContextTypes
from bot import bot
from bot.helper.telegram_helper import Message, Button
from bot.modules.quizzes.quizz_parameters import QuizParameters


class QueryQuizzes:

    async def _query_quizzes_formated_text(update: Update, query, context: ContextTypes.DEFAULT_TYPE):

        formatted_quizzes_message = (f"""
        🎛️ <b>Formatted File Quizzes</b> (Structured Files)
        <i>Create quizzes from a formatted file</i>\n\n
        <b>1. Send number of questions (n) and time limitations (t)</b> 
        <code>(sending numbers and time are optional)</code>
        \t•\t<code>n=questions_num t=time_per_questions</code>\n
        <b>2. Send a Docx file (MS Word) or PDF with <i>pre-formatted questions</i></b>\n
        <b>3. I’ll handle the rest! 😉</b>\n
        <blockquote>Ensure your file follows this format:
        Q1: What is the speed of light?
        A: 299,792 km/s
        B: 120,231 km/s
        C: 200,133 km/s
        D: 100,112 km/s
        Ans: A</blockquote>\n
        <i>💡 For dierct access send this command:</i>\n
        <blockquote>•\t/quiz <code>n=Quiz-Num t=Quiz-Time</code></blockquote>""")


        btn_name_formatted = ["🔙 Back", "✖️ Close"]
        btn_data_formatted = ["query_help_ai_quizzes", "query_close"]

        btn = await Button.cbutton(btn_name_formatted, btn_data_formatted, True, update= update)

        await Message.edit_msg(update, formatted_quizzes_message,
                               query.message, btn)

        # Change bot mode to formatted quiz
        QuizParameters.set_formatted_quiz_mode(context)
        QuizParameters.set_is_premium(context, False)

    async def _query_quizzes_general_text(update: Update, query, context: ContextTypes.DEFAULT_TYPE):
        premium_quizzes_message = ("""
        👑 <b>Premium File Quizzes</b>
        <i>Create quizzes from any resource with specific time and limit using our AI ⚡🤖</i>\n
        <b>1. Send the number of questions (n) and time limitations (t)</b> 
        <code>(sending Question Time is optional)</code>
        \t•\t<code>n=Questions-Num t=Questions-Time</code>\n
        <b>2. Send your quiz study materials:</b>
        \t•\t📜 Files (Docx, PPTX, PDF, TXT, etc.)
        \t•\t🔗 YouTube Video Link
        \t•\t🔉 Audio File\n
        <b>3. I’ll convert it into <code>interactive quizzes</code> for you! 😉</b>\n
        <i>💡 For dierct access send this command:</i>
        <blockquote>•\t/quiz <code>-p n=Quiz-Num t=Quiz-Time</code></blockquote>""")

                                   
        btn_name_row1 = ["👑 Subscribe"]
        btn_data_row1 = ["query_subs"]

        btn_name_row2 = ["🔙 Back", "✖️ Close"]
        btn_data_row2 = ["query_help_ai_quizzes", "query_close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, update= update)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True, update= update)

        btn = row1 + row2

        await Message.edit_msg(update, premium_quizzes_message, query.message,
                               btn)

        # Change bot mode to premium quiz
        QuizParameters.set_premium_quiz_mode(context)
        QuizParameters.set_is_premium(context, True)

    async def _query_quizzes_sanfoundry_text(update: Update, query, context: ContextTypes.DEFAULT_TYPE):
        premium_quizzes_message = ("""
        📖 <b>Sanfoundry Webiste Quizzes</b>
        <i>Create quizzes from <a href='https://www.sanfoundry.com'>Sanfoundry website</a></i>\n
        <b>1. Send the number of questions (n) and time limitations (t)</b> 
        <code>(sending Question Number and Time are optional)</code>
        \t•\t<code>n=Questions-Num t=Questions-Time</code>\n
        <b>2. Send your Sanfoundry link:</b>\n
        <b>3. I’ll convert it into <code>interactive quizzes</code> for you! 😉</b>\n\n
        <i>💡 For dierct access send this command:</i>\n
        <blockquote>•\t/quiz <code>n=Quiz-Num t=Quiz-Time</code></blockquote>""")


        btn_name_row1 = ["👑 Subscribe"]
        btn_data_row1 = ["query_subs"]

        btn_name_row2 = ["🔙 Back", "✖️ Close"]
        btn_data_row2 = ["query_help_ai_quizzes", "query_close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, update= update)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True, update= update)

        btn = row1 + row2

        await Message.edit_msg(update, premium_quizzes_message, query.message,
                               btn)

        # Change bot mode to premium quiz
        QuizParameters.set_sanfoundry_quiz_mode(context)
        
    async def _query_quizzes_databse(update: Update, query, context: ContextTypes.DEFAULT_TYPE):
        pass
