from telegram import Update
from bot import bot
from bot.helper.telegram_helper import Message, Button

class QueryQuizzes:
    async def _query_quizzes_formated_text(update: Update, query):

        formatted_quizzes_message = (
            f"🎛️ <b>Formatted File Quizzes</b> (Structured Files)\n\n"
            f"1. Send <code>/quiz n=numbmer_of_questions t=time_for_questions</code> for 5 questions with 10 min per question\n"
            f"2. Upload a Docx file (MSE Word) with <i>pre-formatted questions</i>\n"
            f"3. I’ll handle the rest! 😉\n"
            f"\t<blockquote>Ensure your file follows this format:\n\n"
            f"\tQ1: What is the speed of light?\n"
            f"\tA: 299,792 km/s\n"
            f"\tB: 120,231 km/s\n"
            f"\tC: 200,133 km/s\n"
            f"\tD: 100,112 km/s\n"
            f"\tAns: A</blockquote>"        )

        btn_name_formatted = ["🔙 Back", "❌ Close"]
        btn_data_formatted = ["query_help_quizzes", "query_close"]

        btn = await Button.cbutton(btn_name_formatted, btn_data_formatted, True)

        await Message.edit_msg(update, formatted_quizzes_message, query.message, btn)


    async def _query_quizzes_general_text(update: Update, query):
        premium_quizzes_message = (
           f"👑 <b>Premium File Quizzes</b>\n\n"
           f"1. Send <code>/quiz n=numbmer_of_questions t=time_for_questions -p</code>\n"
           f"\t <blockquote> <code>/quiz n=5 t=10 -p </code> for 5 questions with 10 min per question\n"
           f"\t <code>/quiz 3 </code> for 3 questions with no timer</blockquote>\n"
           f"2. Upload your quiz file(Any type)\n"
           f"3. I’ll convert it into <i>an interactive quizzes</i> for you!😉\n"
           f"Ready to upload your file? <code>Let’s get quizzing!</code> 🚀"
        )
        btn_name_row1 = ["🔙 Back", "❌ Close"]
        btn_data_row1 = ["query_help_quizzes", "query_close"]

        btn_name_row2 = ["👑 Subscribe"]
        btn_data_row2 = ["query_subs"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2)

        btn = row1 + row2

        await Message.edit_msg(update, premium_quizzes_message, query.message, btn)

    async def _query_quizzes_databse(update: Update, query):
        pass
