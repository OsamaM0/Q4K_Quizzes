import psutil
from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message
from bot.functions.power_users import _power_users


async def func_question_db(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    power_users = await _power_users()
    if user.id not in power_users:
        # await Message.reply_msg(update, "❗ This command is only for bot owner!")
        return

    file_path = "quiz_data.json"
    await context.bot.send_document(
        update.effective_chat.id,
        document=open(file_path, 'rb'),
        caption=f"Your Questions DB")
    