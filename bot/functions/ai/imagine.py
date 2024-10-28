import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message
from bot.modules.database.combined_db import global_search
from bot.modules.safone import Safone
from bot.modules.subs.subs_manger import SubsManager

async def func_imagine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    e_msg = update.effective_message
    prompt = " ".join(context.args)

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

    if not prompt:
        await Message.reply_msg(update, "Use <code>/imagine prompt</code>\nE.g. <code>/imagine a cute cat</code>")
        return

    # Check if there is enough coins for the user
    subs_manager = SubsManager(user.id)

    # Validate user subscription and coin balance using SubsManager
    is_premium_active, remaining_coins = await subs_manager.validate_user_subscription(update, "quiz", context)
    if not is_premium_active:
        return

    sent_msg = await Message.reply_msg(update, "Processing...")
    retry, attempt = 0, 2
    while retry != attempt:
        imagine = await Safone.imagine(prompt)
        if imagine:
            break
        elif retry == attempt:
            await Message.edit_msg(update, "Too many requests! Please try after sometime!", sent_msg)
            return
        retry += 1
        await Message.edit_msg(update, f"Please wait, Imagine is busy!\nAttempt: {retry}/{attempt}", sent_msg)
        await asyncio.sleep(3)
    
    await Message.del_msg(chat.id, sent_msg)
    
    msg = f"» <i>{prompt}</i>"
    if chat.type != "private":
        msg += f"\n<b>Req by</b>: {user.mention_html()}"

    # Pay for the image 
    await subs_manager.use_image_generation()
    coins = await subs_manager.get_remaining_coins()
    msg += f"\n<i><b>Coins Remaining</b>: <code>{coins} Coins 🪙</code></i>"

    
    
    await Message.send_img(chat.id, imagine, msg, tr=False)