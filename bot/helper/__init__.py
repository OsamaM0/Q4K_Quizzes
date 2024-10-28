import asyncio
from bot import bot, logger
from telegram import BotCommand

# commands = [
#     BotCommand("start", "Start the bot")
# ]

command_help = [
    BotCommand("start", "Start Q4K Bot ⚡️"),
    BotCommand("help", "Want some help 🆘"),
    BotCommand("quiz", "Create quiz of your martials ❔"),
    BotCommand("summary", "Create summary of your martials 📑"),
    BotCommand("gpt", "chat with ChatGPT 🤖"),
    BotCommand("imagine", "generate image with your description 🌇"),
    BotCommand("calc", "calculator 🧮"),
    BotCommand("tr", "Translate any thing to any language 🅰️"),
    BotCommand("qr", "Generate QR Code 🏁"),
    BotCommand("id", " Get your ID 🆔"),
    BotCommand("group", "Add bot to your group 👥"),
    BotCommand("invite", "Generate invite link to your group 📨"),
    BotCommand("settings", "Reach to bot Settings ⚙️")
]

class BotCommandHelper:
    def __init__(self, cmd, des):
        self.commad = cmd
        self.description = des

    @staticmethod
    async def set_bot_command():
        try:
            await bot.set_my_commands(command_help)
            logger.info("Bot commands updated!")
        except Exception as e:
            logger.error(e)

asyncio.get_event_loop().run_until_complete(BotCommandHelper.set_bot_command())
