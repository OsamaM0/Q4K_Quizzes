import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import Forbidden
from bot import bot
from bot.helper.telegram_helper import Message, Button
from bot.modules.database.combined_db import find_bot_docs, check_add_user_db
from bot.modules.database.local_database import LOCAL_DATABASE


async def func_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    e_msg = update.effective_message

    if chat.type != "private":
        _bot_info = await bot.get_me()
        sent_msg = await Message.send_msg(user.id, ".")
        if sent_msg == Forbidden:
            await Message.reply_msg(update,
                                    f"Hey, {user.mention_html()}!\n<a href='http://t.me/{_bot_info.username}'>Start me</a> in pm to chat with me!")
            return
        elif sent_msg:
            await Message.reply_msg(update, f"Sent in your pm! <a href='http://t.me/{_bot_info.username}'>Check</a>")
            await Message.del_msg(user.id, sent_msg)

    data = {
        "user_id": user.id,
        "chat_id": chat.id,
        "collection_name": "users",
        "db_find": "user_id",
        "db_vlaue": user.id,
        "edit_data_key": None,
        "edit_data_value": None,
        "del_msg_pointer_id": e_msg.id,
        "edit_data_value_msg_pointer_id": None
    }

    await LOCAL_DATABASE.insert_data("data_center", user.id, data)

    msg = (
        f"🎉 Hey there, {user.mention_html()}! A big warm welcome to the Q4K BOT! 🚀\n\n"
        f"I'm here to make learning fun and seamless with the power of AI! 🎓💡. \n📚👨‍🏫\n\n"
        f"Here are some of the amazing things I can do for you:\n\n"
        f"🔹 Generate dynamic quizzes in seconds ✍️\n"
        f"🔹 Study with our AI-powered tools 🤖📖\n"
        f"🔹 Help teachers manage their groups 👨‍🏫\n"
        f"🔹 And other a variety of features 🌐\n\n"
        f"Let's dive in and get started! 🌟"
    )

    btn_name_row1 = ["📝 Create Quizzes", "🤖 Study with AI Tools"]
    btn_data_row1 = ["query_help_quizzes", "query_help_ai"]

    btn_name_row2 = ["👨‍🏫 Manage Groups", "🌐 Other"]
    btn_data_row2 = ["query_help_group_management", "query_close"]


    btn_name_row3 = ["ℹ️ Information", "🛑 Help"]
    btn_data_row3 = ["query_help_bot_info", "query_close"]

    row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
    row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
    row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)

    btn = row1 + row2 + row3

    _bot = await find_bot_docs()
    if not _bot:
        return

    images = _bot.get("images")
    if images:
        image = random.choice(images).strip()
    else:
        image = _bot.get("bot_pic")

    if image:
        await Message.send_img(user.id, image, msg, btn)
    else:
        await Message.send_msg(user.id, msg, btn)

    await check_add_user_db(user)
