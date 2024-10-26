from telegram import Update
from bot import bot
from bot.helper.telegram_helper import Message, Button
from bot.modules.database.mongodb import MongoDB


class QueryBotHelp:

    async def _query_help_group_management(update: Update, query):
        msg = (
            f"""
                    👥  <b>Group Management</b>\n
                    <i>Managing your group has never been easier!</i>\n\n
                    Whether you're \n
                    *\t<b>creating a collaborative space for students</b> \n
                    *\t<b>keeping communication focused</b>,\n\n
                    these powerful commands will help you <b>maintain control with ease and efficiency</b> 🚀."""
        )
        btn_name_row1 = ["👥 Group", "🧑‍🎓 Student"]
        btn_data_row1 = ["query_group_group_management", "query_group_student_management"]

        btn_name_row2 = ["📨 Message", "⚙️ Settings"]
        btn_data_row2 = ["query_group_message_management", "query_chat_settings_menu"]
        
        btn_name_row3 = ["🔙 Back", "✖️ Close"]
        btn_data_row3 = ["query_help_menu", "query_close"]

        btn_1 = await Button.cbutton(btn_name_row1, btn_data_row1, True, update= update)
        btn_2 = await Button.cbutton(btn_name_row2, btn_data_row2, True, update= update)
        btn_3 = await Button.cbutton(btn_name_row3, btn_data_row3, True, update= update)

        btn = btn_1 + btn_2 + btn_3

        await Message.edit_msg(update, msg, query.message, btn)


    async def _query_help_ai(update: Update, query):
        
        msg = (f"""
                  ⚡<b>Welcome to Study with AI!</b> 🚀\n<i>Your ultimate AI-powered study companion, Study smarter with AI 📚⚡</i>\n
                 <blockquote><b>📝 Quiz Generator:\n</b> Instantly create personalized quizzes to test and reinforce your knowledge.</blockquote>
                 <blockquote><b>📖 Summury Generator:\n</b> Summarize any study materials you have in seconds.</blockquote>
                 <blockquote><b>⚡ Chat with ChatGPT :\n</b> Ask any academic question, and get clear, accurate responses powered by ChatGPT.</blockquote> 
                 <blockquote><b>🌇 Image Generator :\n</b> Describe whatever image you want to generate powered by Stable Diffusion.</blockquote> """)
        btn_name_row1 = ["📝Quiz Generator", "📖 Summury Generator"]
        btn_data_row1 = ["query_help_ai_quizzes", "query_help_ai_summarize"]

        btn_name_row2 = ["⚡ Chat GPT", "🌇 Image Generator"]
        btn_data_row2 = ["query_help_ai_gpt", "query_help_ai_imagine"]

        btn_name_row3 = ["👑 Subscription"]
        btn_data_row3 = ["query_subs"]
        
        btn_name_row4 = ["🔙 Back", "✖️ Close"]
        btn_data_row4 = ["query_help_menu", "query_close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, update= update)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True, update= update)
        row3 = await Button.cbutton(btn_name_row3, btn_data_row3, update= update)
        row4 = await Button.cbutton(btn_name_row4, btn_data_row4, True, update= update)
        

        btn = row1 + row2 + row3 + row4

        await Message.edit_msg(update, msg, query.message, btn)

    async def _query_help_stdtools(update: Update, query):
        msg = (
            f"""
               💡 <b>Welcome to Student Tools!</b> 🛠️\n <i>Your essential toolkit for students, all in one place! Maximize your productivity with smart tools 🧠✨</i>\n
               <b>Explore the tools designed to make your student life easier:</b>\n
             <blockquote><b>🎥 YouTube Download:\n</b> Download YouTube videos for offline access and seamless studying.</blockquote>
             <blockquote><b>🔍 YouTube Search:\n</b> Quickly search for educational videos and tutorials on YouTube.</blockquote>
             <blockquote><b>🌐 Translator:\n</b> Translate any text into multiple languages to aid your learning.</blockquote>
             <blockquote><b>🧮 Calculator:\n</b> Solve complex equations with an easy-to-use calculator.</blockquote>
             <blockquote><b>📲 QR Code Generator:\n</b> Create and share QR codes instantly for any link or information.</blockquote>"""
             # <blockquote><b>📸 Webshot:\n</b> Capture screenshots of any website for later reference.</blockquote>
        )
        btn_name_row1 = ["🎥 YouTube Download", "🔍 YouTube Search"]
        btn_data_row1 = ["query_help_stdtools_youtube_download", "query_help_youtube_search"]

        # btn_name_row2 = ["🌐 Translator", "🧮 Calculator", "📲 QR Code", "📸 Webshot"]
        # btn_data_row2 = ["query_help_stdtools_translator", "query_help_stdtools_calculator", "query_help_stdtools_qr_code_generator", "query_help_stdtools_webshot"]
        btn_name_row2 = ["🌐 Translator", "🧮 Calculator", "📲 QR Code"]
        btn_data_row2 = ["query_help_stdtools_translator", "query_help_stdtools_calculator", "query_help_stdtools_qr_code_generator"]
        
        btn_name_row3 = ["🔙 Back", "✖️ Close"]
        btn_data_row3 = ["query_help_menu", "query_close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True, update= update)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True, update= update)
        row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True, update= update)
        
        btn = row1 + row2 + row3

        await Message.edit_msg(update, msg, query.message, btn)


    async def _query_help_misc_functions(update: Update, query):
        msg = (
            "<b>Misc functions</b>\n\n"
            "/movie » get any movie info by name or imdb id\n"
            "/tr » translate any language\n"
            "/decode » convert base64 into text\n"
            "/encode » convert text into base64\n"
            "/short » short any url\n"
            "/ping » ping any url\n"
            "/calc » calculate any math (supported syntex: +, -, *, /)\n"
            "/webshot » take screenshot of any website\n"
            "/weather » get weather info of any city\n"
            "/ytdl » download youtube video\n"
            "/yts » search video on youtube\n"
            "/qr » generate a QR code\n"
            "/itl » convert image into a public link\n"
            "/whisper » secretly tell something to someone in group chat\n"
            "/id » show chat/user id\n"
            "/settings » settings of chat\n\n"
            "<i><b>Note:</b> Send command to get more details about the command functions!</i>"
        )

        btn_name = ["Back", "Close"]
        btn_data = ["query_help_menu", "query_close"]
        btn = await Button.cbutton(btn_name, btn_data, True, update= update)

        await Message.edit_msg(update, msg, query.message, btn)


    async def _query_help_owner_functions(update: Update, query):
        msg = (
            "<b>Bot owner functions</b>\n\n"
            "/broadcast » broadcast message to all active users\n"
            "/db » get bot database\n"
            "/bsettings » get bot settings\n"
            "/shell » use system shell\n"
            "/log » get log file (for error handling)\n"
            "/restart » restart the bot (use with caution ⚠)\n"
            "/sys » get system info\n\n"
            "<i><b>Note:</b> Send command to get more details about the command functions!</i>"
        )

        btn_name = ["Back", "Close"]
        btn_data = ["query_help_menu", "query_close"]
        btn = await Button.cbutton(btn_name, btn_data, True, update= update)

        await Message.edit_msg(update, msg, query.message, btn)
    

    async def _query_help_bot_info(update: Update, query):
        _bot_info = await bot.get_me()
        info_db = await MongoDB.info_db()
        total_users = "~"
        for i in info_db:
            if i[0] == "users":
                total_users = i[1]
                break
        
        active_status = await MongoDB.find("users", "active_status")
        active_users = active_status.count(True)
        inactive_users = active_status.count(False)

        msg = (
            f"""
                <blockquote><b>• Name:\t</b> {_bot_info.full_name}</blockquote>
                <blockquote><b>• Username:\t</b> {_bot_info.name}</blockquote>
                <blockquote><b>• Registered users:\t</b> <code>{total_users}</code></blockquote>
                <blockquote><b>• Active users:\t</b> <code>{active_users}</code></blockquote>
                <blockquote><b>• Inactive users:\t</b> <code>{inactive_users}</code></blockquote>
                <blockquote><b>• Developer:\t</b> <a href='https://t.me/osama_mo7'>Osama Mo</a></blockquote>"""
        )

        btn_name = ["Back", "Close"]
        btn_data = ["query_help_menu", "query_close"]
        btn = await Button.cbutton(btn_name, btn_data, True, update= update)

        await Message.edit_msg(update, msg, query.message, btn)
