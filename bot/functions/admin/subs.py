import psutil
from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message
from bot.functions.power_users import _power_users
from bot.modules.subs.subs_manger import SubsManager

async def func_subs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # try:
        user = update.effective_user
        subs_user_id, coins_num, monthes = context.args
        
        power_users = await _power_users()
        if user.id not in power_users:
            # await Message.reply_msg(update, "❗ This command is only for bot owner!")
            return
    
        subs_manager = SubsManager(int(subs_user_id))
    
        await subs_manager.subscriber_user(True, int(monthes) ,int(coins_num))
    
        await Message.reply_msg(update, f"Added {coins_num} coins with {monthes} month to user {subs_user_id} 🥳")
    
    # except Exception as e:
    #     print("ERROR: ", e)
    #     return