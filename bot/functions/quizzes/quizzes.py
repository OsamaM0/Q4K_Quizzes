import re
from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message, Button
from bot.modules.database.combined_db import global_search
from bot.modules.subs.subs_manger import SubsManager
from bot.modules.quizzes.quizz_parameters import QuizParameters


async def extract_quiz_args(args, update):
    """Extracts quiz arguments like question number and timer from user input."""
    question_num = question_timer = -1
    if not args:
        e_msg = update.message.text_html or update.message.caption_html if update.message else None
        args = e_msg.split(" ")
    for part in args:
        try:
            if "n" in part:
                question_num = int(re.findall(r'\d+', part)[0])
            elif "t" in part:
                question_timer = int(re.findall(r'\d+', part)[0])
        except ValueError:
            return None, None
    return question_num, question_timer



async def handle_quiz_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    e_msg = update.effective_message

    # Extract and validate user arguments
    question_num, question_timer = await extract_quiz_args(context.args, update)
    if question_num is None or question_timer is None:
        await Message.reply_msg(
            update,
            "Please send valid digit numbers for <b>Question Number</b> or <b>Timer</b>. "
            "Like <code>/quiz n=5 t=10</code> (No spaces between argument and value)."
        )
        return
    elif question_num == -1 and QuizParameters.get_is_premium(context):
        await Message.reply_msg(update, "Please send valid digit numbers for <b>Question Number</b>.\n<blockquote>Like <code>n=5</code></blockquote>")
        return
        
    if context.args:
        is_premium_quiz = '-p' in context.args
    else:
        is_premium_quiz = QuizParameters.get_is_premium(context)

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

    # Deduct the coins from the user's balance using SubsManager
    subs_manager = SubsManager(update.effective_chat.id)

    # Validate user subscription and coin balance using SubsManager
    is_premium_active, remaining_coins = await subs_manager.validate_user_subscription(update, "quiz", context)
    if not is_premium_active:
        return

    # Get remaining days for the premium subscription
    remaining_days = await subs_manager.get_remaining_premium_days()

    # Set quiz parameters
    if is_premium_quiz:
        QuizParameters.set_premium_quiz_mode(context)
    else:
        QuizParameters.set_formatted_quiz_mode(context)
    QuizParameters.set_question_num(context, question_num)
    QuizParameters.set_question_timer(context, question_timer)
    QuizParameters.set_is_premium(context, is_premium_quiz)
    
    # Prepare the response message
    msg_txt = "You now will use <b>{}</b>\n".format(
        "Premium File Quizzes Generator ✨️" if is_premium_quiz else "Formatted File Quizzes Generator 🎛️"
    )

    if is_premium_quiz:
        msg_txt += "\nYou are on the <b>Premium Plan</b>." if is_premium_active else "\nYou are on the <b>Free Plan</b>."
        msg_txt += f" Your subscription expires in <b>{remaining_days} days</b> with <b>{remaining_coins}</b> questions remaining."

    msg_txt += f"\n<blockquote>You chose {question_num if question_num != -1 else 'No limit'} questions"
    msg_txt += f" with {f'{question_timer} minutes' if question_timer != -1 else 'No time'}</blockquote>"
    msg_txt += "Please send any of your studying materials."

    await Message.reply_msg(update, msg_txt)
