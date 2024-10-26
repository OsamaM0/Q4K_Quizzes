from telegram import Update
from bot import bot
from bot.modules.database.mongodb import MongoDB
from bot.helper.telegram_helper import Message, Button
from datetime import datetime
class QuerySubs:
    async def _query_subs(update: Update, query):
        """Validates user subscription and premium status."""
        find_user = await MongoDB.find_one("users", "user_id", update.effective_chat.id)
        msg = ""
    
        if not find_user:
            await Message.reply_msg(update, "User data not found.")
            return
    
        is_premium_user = find_user.get("premium", False)
    
        if is_premium_user:
            # Message for Premium Users
            reminig_premium_days = datetime.fromisoformat(find_user.get("premium_expiration")) - datetime.utcnow()
            reminig_premium_days = reminig_premium_days.days
            user_reminig_premium_quizzes = find_user.get("reminig_premium_quizzes")
    
            msg = (
                    f"""
                    <b>Subscription Status:</b> ⭐\n
                    <i>You are a premium user! Enjoy full access to all tools and features.</i>\n\n
                    <blockquote><b>Premium Details:</b>\n
                    <b>Days remaining:</b> {reminig_premium_days} days\n
                    <b>Remaining premium Coins:</b> {user_reminig_premium_quizzes} 🪙</blockquote>"""
                )
        else:
            # Message for Non-Premium Users
            msg = (
                f"""<b>Subscription Status:</b> ⚠️\n
                <i>You are not a premium user.</i>\n\n
                <blockquote><b>Upgrade to premium to unlock all features!</b>\n
                Enjoy unlimited quizzes, full tool access, and more.</blockquote>"""
            )
        btn_name_row1 = ["👑 Subscriptions Prices"]
        btn_data_row1 = ["query_subs_prices"]

        btn_name_row2 = ["Contact me (Osama M0)"]
        btn_data_row2 = ["https://t.me/OSAMA_MO7"]

        btn_name_row3 = ["🔙 Back", "✖️ Close"]
        btn_data_row3 = ["query_help_ai_quizzes", "query_close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, update= update)
        row2 = await Button.ubutton(btn_name_row2, btn_data_row2, True, update= update)
        row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True,  update= update)

        btn = row1 + row2 + row3

    
    
        await Message.edit_msg(update, msg, query.message, btn)
    
    async def _query_subs_prices(update: Update, query):
        """Shows the user the subscription prices."""
        msg = (
            f"""<b>✨ Q4K Bot Subscriptions ✨</b>\n\n
            <i>Choose the right plan for you and enjoy premium features at a discounted rate!</i>\n\n
            <blockquote><b>🎓 Student Plan:</b>\n
            - Price: $15\n
            - Includes 2,000 🪙 coins</blockquote>\n
            <blockquote><b>👨‍🏫 Teacher Plan:</b>\n
            - Price: $30\n
            - Includes 10,000 🪙 coins</blockquote>\n
            <blockquote><b>🏢 Institution Plan:</b>\n
            - Price: $50\n
            - Includes 40,000 🪙 coins</blockquote>\n
            <blockquote><b>🏫 Institution+ Plan:</b>\n
            - Price: $100\n
            - Includes 100,000 🪙 coins</blockquote>\n
            <i>These subscriptions are available at a limited-time discount of 80% from 2024/10 to 2024/12.</i>\n\n
            <b>💰 Coin Usage:</b>\n
            <blockquote>- 1 Premium Question = 1 🪙 coin\n
            - 1 Summarization = 10 🪙 coins\n
            - 1 Image Generation = 5 🪙 coins\n
            - 1 Question Ask = 2 🪙 coins</blockquote>"""
        )
    
        btn_name_formatted = ["🔙 Back", "✖️ Close"]
        btn_data_formatted = ["query_subs", "query_close"]
    
        btn = await Button.cbutton(btn_name_formatted, btn_data_formatted, True, update= update)
    
        await Message.edit_msg(update, msg, query.message, btn)
    