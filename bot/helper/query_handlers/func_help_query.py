from telegram import Update
from bot import bot
from bot.helper.telegram_helper import Message, Button
from bot.modules.database.mongodb import MongoDB


class QueryBotHelp:
    async def _query_help_quizzes(update: Update, query):
        quizzes_message = (
            f"🎯 <b>Welcome to the Quiz Hub!</b>\n"
            f"Ready to challenge yourself or your group? Pick a quiz type and let's get started! 🧠✨\n"
            f"1️⃣ <b>Quizzes in Database</b>: Access ready-made quizzes from our collection. 📚\n"
            f"2️⃣ <b>Premium File Quizzes</b>: Upload your files and get premium quizzes from normal text. 💼📄\n"
            f"3️⃣ <b>Formatted File Quizzes</b>: Need more structure? Upload files with formatted questions! 🎛️📝\n"
            f"Choose your option below and let's quiz away! 🚀"
        )

        btn_name_row1 = ["📚 Database", "🎛️ Formatted Files" ]
        btn_data_row1 = ["query_quiz_database", "query_quizzes_formated_text"]

        btn_name_row2 = ["👑 Premium (Normal Files)"]
        btn_data_row2 = ["query_quiz_general_files"]

        btn_name_row3 = ["🔙 Back", "✖️ Close"]
        btn_data_row3 = ["query_help_menu", "query_close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, )
        row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)

        btn = row1 + row2 + row3

        await Message.edit_msg(update, quizzes_message, query.message, btn)



    async def _query_help_group_management(update: Update, query):
        msg = (
            "<b>Group Moderation Commands</b>\n\n"
            "/id » Show chat/user id\n"
            "/invite » Generate chat invite link\n"
            "/promote | /fpromote » promote a member ('f' means with full privilege)\n"
            "/apromote | /fapromote » <code>anonymously</code> promote/fpromote a member\n"
            "/demote » demote a member\n"
            "/pin » pin replied message loudly\n"
            "/unpin » unpin a pinned message\n"
            "/unpinall » unpin all pinned messages"
            "/ban » ban a member\n"
            "/unban » unban a member\n"
            "/kick » kick a member\n"
            "/kickme » The easy way to out\n"
            "/mute » restrict a member (member will be unable to send messages etc.)\n"
            "/unmute » unrestrict a restricted member\n"
            "/del » delete the replied message with a warning!\n"
            "/purge » delete every messages from replied to current message!\n"
            "/lock » lock the chat (member will be unable to send messages etc.)\n"
            "/unlock » unlock the chat (back to normal)\n"
            "/filters | /filter | /remove » to see/set/remove custom message/command\n"
            "/adminlist » to see chat admins list\n"
            "/settings » settings of chat\n\n"
            "<i><b>Note:</b> Some command has a silent function! eg. <code>/s[command]</code> » /sban etc.</i>\n\n"
        )

        btn_name = ["Back", "Close"]
        btn_data = ["query_help_menu", "query_close"]
        btn = await Button.cbutton(btn_name, btn_data, True)

        await Message.edit_msg(update, msg, query.message, btn)


    async def _query_help_ai(update: Update, query):
        msg = (
            "<b>Artificial intelligence</b>\n\n"
            "/imagine » generate AI image\n"
            "/gpt » ask any question to ChatGPT\n\n"
            "<i><b>Note:</b> Send command to get more details about the command functions!</i>"
        )

        btn_name = ["Back", "Close"]
        btn_data = ["query_help_menu", "query_close"]
        btn = await Button.cbutton(btn_name, btn_data, True)

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
        btn = await Button.cbutton(btn_name, btn_data, True)

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
        btn = await Button.cbutton(btn_name, btn_data, True)

        await Message.edit_msg(update, msg, query.message, btn)
    

    async def _query_help_bot_info(update: Update, query):
        _bot_info = await bot.get_me()
        info_db = await MongoDB.info_db()
        for i in info_db:
            if i[0] == "users":
                total_users = i[1]
                break
            else:
                total_users = "~"
        
        active_status = await MongoDB.find("users", "active_status")
        active_users = active_status.count(True)
        inactive_users = active_status.count(False)

        msg = (
            "<b><code>» bot.info()</code></b>\n\n"

            f"<b>• Name:</b> {_bot_info.full_name}\n"
            f"<b>• ID:</b> <code>{_bot_info.id}</code>\n"
            f"<b>• Username:</b> {_bot_info.name}\n\n"

            f"<b>• Registered users:</b> <code>{total_users}</code>\n"
            f"<b>• Active users:</b> <code>{active_users}</code>\n"
            f"<b>• Inactive users:</b> <code>{inactive_users}</code>\n\n"

            "<b>• Source code:</b> <a href='https://github.com/bishalqx980/tgbot'>GitHub</a>\n"
            "<b>• Developer:</b> <a href='https://t.me/bishalqx980'>bishalqx980</a>"
        )

        btn_name = ["Back", "Close"]
        btn_data = ["query_help_menu", "query_close"]
        btn = await Button.cbutton(btn_name, btn_data, True)

        await Message.edit_msg(update, msg, query.message, btn)
