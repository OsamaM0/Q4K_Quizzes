import asyncio
import re
from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message
from bot.modules.database.combined_db import global_search
from bot.modules.database.mongodb import MongoDB
from bot.modules.quizzes.quizz_parameters import QuizParameters


async def extract_quiz_args(args):
    """Extracts quiz arguments like question number and timer from user input."""
    question_num = question_timer = 0
    for part in args:
        try:
            if "n" in part:
                question_num = int(re.findall(r'\d+', part)[0])
            elif "t" in part:
                question_timer = int(re.findall(r'\d+', part)[0])
        except ValueError:
            return None, None
    return question_num, question_timer


async def validate_user_subscription(update, user, is_premium):
    """Validates user subscription and premium status."""
    db = await global_search("users", "user_id", user.id)
    if not db[0]:
        await Message.reply_msg(update, db[1])
        return None, None

    find_user = db[1]
    if not is_premium:
        return find_user, None

    if find_user.get("reminig_premium_days", 0) <= 0 or find_user.get("reminig_premium_quizzes", 0) <= 0:
        await Message.reply_msg(update, "Your subscription or quiz limit has expired! Please contact @Osama_mo7 for renewal.")
        await MongoDB.update_db("users", "user_id", user.id, "premium", False)
        return None, None

    return find_user, find_user.get("premium")


async def handle_quiz_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    e_msg = update.effective_message

    # Extract and validate user arguments
    question_num, question_timer = await extract_quiz_args(context.args)
    if question_num is None or question_timer is None:
        await Message.reply_msg(
            update,
            "Please send valid digit numbers for <b>Question Number</b> or <b>Timer</b>. "
            "Like <code>/quiz n=5 t=10</code> (No spaces between argument and value)."
        )
        return

    is_premium = '-p' in context.args

    # Check if AI chat is enabled in non-private chats
    if chat.type != "private":
        db = await global_search("groups", "chat_id", chat.id)
        if not db[0]:
            await Message.reply_msg(update, db[1])
            return

        ai_status = db[1].get("ai_status")
        if ai_status is False:
            await Message.del_msg(chat.id, e_msg)
            return

    # Validate user subscription status
    find_user, user_premium = await validate_user_subscription(update, user, is_premium)
    if find_user is None:
        return

    # Set quiz parameters
    user_reminig_premium_quizzes = find_user.get("reminig_premium_quizzes", 0)
    question_num = min(user_reminig_premium_quizzes, question_num) if is_premium else question_num

    QuizParameters.set_question_num(question_num)
    QuizParameters.set_question_timer(question_timer)
    QuizParameters.set_is_quiz(True)

    # Prepare the response message
    msg_txt = "You now will use <b>{}</b>\n".format(
        "Premium File Quizzes Generator ✨️" if is_premium else "Formatted File Quizzes Generator 🎛️"
    )

    if is_premium:
        msg_txt += f"\nYour subscription expires in <b>{find_user.get('reminig_premium_days')} days</b>" \
                   f"\nRemaining questions: <b>{user_reminig_premium_quizzes} questions</b>"
    else:
        msg_txt += "\nYou are on the Free Plan. You have 10 questions for 1 time."

    msg_txt += f"\n<blockquote>You chose {question_num if question_num != 0 else 'No limit'} questions"
    msg_txt += f" with {f'{question_timer} minutes' if question_timer != 0 else 'No time'}</blockquote>"
    msg_txt += "Please send your file."

    await Message.reply_msg(update, msg_txt)
