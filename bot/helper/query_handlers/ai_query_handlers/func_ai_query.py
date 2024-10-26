from telegram import Update
from bot import bot
from bot.helper.telegram_helper import Message, Button
from bot.modules.quizzes.quizz_parameters import QuizParameters
from telegram.ext import ContextTypes
from bot.modules.subs.subs_manger import SubsManager


class QueryAI:

    async def _query_help_ai_quizzes(update: Update, query):
        quizzes_message = (f"""
                            🎯 <b>Welcome to the Quiz Generator🚀</b>\n
                            <i>Ready to challenge yourself or your group? Pick a quiz type and let's get started! 🧠✨</i>\n\n
                            <b>Choose your Quiz Generator type: </b>\n
                            <blockquote>1️⃣ <b>Premium Quizzes</b>:\nUpload any thing and get premium quizzes using our AI. 🤖📄</blockquote>
                            <blockquote>2️⃣ <b>Formatted Quizzes</b>:\npload files with formatted questions! 🎛️📝</blockquote>
                            <blockquote>3️⃣ <b>Database Quizzes</b>:\nAccess ready-made quizzes from our collection. 🗃️📚\n</blockquote>"""
                                           )

        btn_name_row1 = [
            "👑 Premium Quizzes", "🎛️ Formatted Quizzes", "📖 Sanfoundry website"
        ]
        btn_data_row1 = [
            "query_quiz_general_files", "query_quizzes_formated_text",
            "query_quizzes_sanfoundry_text"
        ]

        btn_name_row2 = ["🔙 Back", "✖️ Close"]
        btn_data_row2 = ["query_help_ai", "query_close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, update= update)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True, update= update)

        btn = row1 + row2

        await Message.edit_msg(update, quizzes_message, query.message, btn)

        

    async def _query_help_ai_summarize(update: Update, query, context: ContextTypes.DEFAULT_TYPE):
        quizzes_message = (f"""
                            🎯 <b>Welcome to the Q4K Summarize🚀</b>\n
                            <i>Ready to summarize your study materials📑? Pick a whatever your study materials and let's get started! 🧠✨</i>\n\n
                            <b>Send your any of your study materials:</b>\n\t
                            \t•\t 📜 Files (Docx, PPTX, PDF, TXT, etc.)
                            \t•\t 🔗 YouTube Video Link
                            \t•\t 🔉 Audio File\n\t
                            <b>I’ll give you an <code> summarization text</code> of your materials!</b>😉\n
                            <blockquote><b>You can acces dierct to Q4K Summarize by Sending this command</b>\n
                            \t•\t/summary </blockquote>""")

        btn_name_row1 = ["👑 Your Subscription"]
        btn_data_row1 = ["query_subs"]

        btn_name_row2 = ["🔙 Back", "✖️ Close"]
        btn_data_row2 = ["query_help_ai", "query_close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, update= update)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True, update= update)

        btn = row1 + row2

        await Message.edit_msg(update, quizzes_message, query.message, btn)

        # Deduct the coins from the user's balance using SubsManager
        subs_manager = SubsManager(update.effective_chat.id)

        # Validate user subscription and coin balance using SubsManager
        is_premium_active, remaining_coins = await subs_manager.validate_user_subscription(update, "summary", context)
        


    
    async def _query_help_ai_chat(update: Update, query):
        quizzes_message = (f"""
                            🎯 <b>Welcome to the Q4K Chat🚀</b>\n
                            <i>Ready to chat with your study materials? Pick a whatever your study materials and let's get started! 🧠✨</i>\n\n
                            <b>Send your any of your study materials:</b>\n\t
                                \t•\t 📜 Files (Docx, PPTX, PDF, TXT, etc.)
                                \t•\t 🔗 YouTube Video Link
                                \t•\t 🔉 Audio File\n
                               <b>I’ll give you an <code> summarization text</code> of your materials!</b>😉\n
                               <blockquote><b>You can acces dierct to Q4K Summarize by Sending this command</b>\n
                                           \t•\t/chat </blockquote>""")
    
        btn_name_row1 = ["👑 Your Subscription"]
        btn_data_row1 = ["query_subs"]
    
        btn_name_row2 = ["🔙 Back", "✖️ Close"]
        btn_data_row2 = ["query_help_ai", "query_close"]
    
        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, update= update)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True, update= update)
    
        btn = row1 + row2
    
        await Message.edit_msg(update, quizzes_message, query.message, btn)

        # Deduct the coins from the user's balance using SubsManager
        subs_manager = SubsManager(update.effective_chat.id)

        # Validate user subscription and coin balance using SubsManager
        is_premium_active, remaining_coins = await subs_manager.validate_user_subscription(update, "chat", context)



    async def _query_help_ai_gpt(update: Update, query, context: ContextTypes.DEFAULT_TYPE):
        quizzes_message = (f"""
                            🎯 <b>Welcome to the Q4K ChatGPT🚀</b>\n
                            <i>Ready to chat with your our AI Model powered by GPT? let's get started! 🧠✨</i>\n\n
                            <b>To use Q4K chatGPT send command</b>
                                    <blockquote>\t•\t/gpt <code>your query</code> </blockquote>\n
                                    <b>I’ll give you an <code> response text to your query </code>!</b>😉\n""")
    
        btn_name_row1 = ["👑 Your Subscription"]
        btn_data_row1 = ["query_subs"]
    
        btn_name_row2 = ["🔙 Back", "✖️ Close"]
        btn_data_row2 = ["query_help_ai", "query_close"]
    
        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, update= update)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True, update= update)
    
        btn = row1 + row2
    
        await Message.edit_msg(update, quizzes_message, query.message, btn)
        
        # Deduct the coins from the user's balance using SubsManager
        subs_manager = SubsManager(update.effective_chat.id)

        # Validate user subscription and coin balance using SubsManager
        is_premium_active, remaining_coins = await subs_manager.validate_user_subscription(update, "gpt", context)

        
    async def _query_help_ai_imagine(update: Update, query, context: ContextTypes.DEFAULT_TYPE):
        quizzes_message = (f"""
                            🎯 <b>Welcome to the Q4K Imagine 🚀</b>\n
                            <i>Ready to an image powered by Stable Diffusion? let's get started! 🧠✨</i>\n\n
                            <b>To use Q4K Imagine send command</b>
                            <blockquote>\t•\t/imagine <code>description of your image</code></blockquote> \n
                            <b>I’ll give you <code> a image you ask for </code>!</b>😉""")

        btn_name_row1 = ["👑 Your Subscription"]
        btn_data_row1 = ["query_subs"]

        btn_name_row2 = ["🔙 Back", "✖️ Close"]
        btn_data_row2 = ["query_help_ai", "query_close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, update= update)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True, update= update)

        btn = row1 + row2

        await Message.edit_msg(update, quizzes_message, query.message, btn)

        # Deduct the coins from the user's balance using SubsManager
        subs_manager = SubsManager(update.effective_chat.id)

        # Validate user subscription and coin balance using SubsManager
        is_premium_active, remaining_coins = await subs_manager.validate_user_subscription(update, "imagine", context)
