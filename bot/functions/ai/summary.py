from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message
from bot.modules.database.combined_db import global_search
from bot.modules.quizzes.quizz_parameters import QuizParameters
from bot.modules.subs.subs_manger import SubsManager


async def func_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    e_msg = update.effective_message

    if chat.type != "private":
        db = await global_search("groups", "chat_id", chat.id)
        if db[0] == False:
            await Message.reply_msg(update, db[1])
            return

        find_group = db[1]

        ai_status = find_group.get("ai_status")
        if not ai_status and ai_status != None:
            await Message.del_msg(chat.id, e_msg)
            return

    # Check if there is enough coins for the user
    # Deduct the coins from the user's balance using SubsManager
    subs_manager = SubsManager(update.effective_chat.id)

    # Validate user subscription and coin balance using SubsManager
    is_premium_active, remaining_coins = await subs_manager.validate_user_subscription(update, "quiz", context)
    if not is_premium_active:
        return

    # Send message to user
    await Message.reply_msg(update, f"""<b>Please Send any of you'r study materials, whatever it was:</b>
                                        \n\t•\Files (Docx, PPTX, PDF, TXT, etc.)
                                        \n\t•YouTube Video Link
                                        \n\t•Audio File
                                        \n\n<i>I will give you an <code> Docx File</code> have your summarized text</i>😉\n""")    
