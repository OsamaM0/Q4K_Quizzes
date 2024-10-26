from telegram import Update
from bot import bot
from bot.helper.telegram_helper import Message, Button


class QueryStdTools:

    async def _query_stdtools(update: Update, query):

        msg = ""

        if query.data  == "query_help_stdtools_youtube_download":
            msg = (f"""
                    <b>YouTube Download:</b> 🎥\n
                    <i>Download YouTube videos effortlessly for offline viewing.</i>\n\n
                    <blockquote><b>Usage:\n</b> /ytdl <code>youtube_url</code>\n
                    E.g. \n<code>/ytdl https://youtube.com/bc123456789</code></blockquote>""")
            
        elif query.data  == "query_help_youtube_search":
            msg = (f"""
                    <b>YouTube Search:</b> 🔍\n
                    <i>Quickly search YouTube for educational content or tutorials.</i>\n\n
                    <blockquote><b>Usage:\n</b> /yts <code>keyword</code>\n
                    E.g.\n <code>/yts google keynote</code></blockquote>""")
            
        elif query.data  == "query_help_stdtools_translator":
            msg = (f"""
                    <b>Translator:</b> 🌐\n
                    <i>Translate text instantly into any language of your choice.</i>\n\n
                    <blockquote><b>Translation of a specific text:</b>\n\t•\t /tr <code>text</code> \n\t•\t /tr <code>lang_code text</code></blockquote>\n
                    <blockquote><b>Translation of a specific Message:</b>\n Reply to a message with \n\t•\t /tr \n\t•\t /tr <code> lang_code</code></blockquote>\n
                    <i>Tip: Enable auto-translation from /settings.</i>""")
            
        elif query.data  == "query_help_stdtools_calculator":
            msg = (f"""
                    <b>Calculator:</b> 🧮\n
                    <i>Perform quick calculations with ease, no matter how complex.</i>\n\n
                    <blockquote><b>Usage:\n\t•\t</b> /calc\t<code>math_expression</code>\n
                    \t•reply to a message containing a math expression with \n\t•\t /calc\n
                    E.g.\n<code>/calc (980 - 80) + 100 / 4 * 4 - 20</code></blockquote>""")
            
        elif query.data  == "query_help_stdtools_qr_code_generator":
            msg = (f"""
                    <b>QR Code Generator:</b> 📲\n
                    <i>Generate QR codes for any text, data, or link instantly.</i>\n\n
                    <blockquote><b>Usage:\n</b> /qr <code>url/data/text</code>\n
                    E.g. \n<code>/qr https://google.com</code></blockquote>""")

        elif query.data  == "query_help_stdtools_webshot":
            msg = (f"""
                    <b>Webshot:</b> 📸\n
                    <i>Take screenshots of any website in an instant.</i>\n\n
                    <blockquote><b>Usage:\n</b> /webshot <code>url</code>\n
                    E.g. \n<code>/webshot https://google.com</code></blockquote>"""
                   )

        btn_name_formatted = ["🔙 Back", "✖️ Close"]
        btn_data_formatted = ["query_help_stdtools", "query_close"]

        btn = await Button.cbutton(btn_name_formatted, btn_data_formatted, True, update= update)

        await Message.edit_msg(update, msg, query.message, btn)
