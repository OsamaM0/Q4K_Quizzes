from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot import logger
from bot.helper.telegram_helper import Message, Button, Quiz
from bot.modules.database.combined_db import global_search
from bot.modules.database.local_database import LOCAL_DATABASE
from bot.modules.quizzes.quizz_parameters import QuizParameters
from bot.modules.translator import translate
from bot.functions.group_management.check_permission import _check_permission
from bot.modules.re_link import RE_LINK
from bot.modules.base64 import BASE64
from bot.modules.text_extractor.text_extractor import TextExtractor
from bot.modules.mcq_generator.text_to_mcq_manager import TextToMCQ
import os


async def func_filter_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("FILE SENT")
    # previous_msg = await Message.get_previous_message(update, context)
    # print(previous_msg)
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message
    print(e_msg)
    msg = update.message.text_html or update.message.caption_html if update.message else None
    document = update.message.document

    if not msg and not document:
        return

    if user.id == 777000:  # Telegram channel
        return

    data_center = await LOCAL_DATABASE.find_one("data_center", chat.id)
    if data_center:
        is_editing = data_center.get("is_editing")  # bool
        if is_editing:
            try:
                msg = int(msg)
            except:
                msg = msg

            for key, value in zip(["edit_data_value", "edit_data_value_msg_pointer_id", "is_editing"],
                                  [msg, e_msg.id, False]):
                await LOCAL_DATABASE.insert_data("data_center", chat.id, {key: value})
            return

    # If a document is sent
    if document:

        if QuizParameters.get_is_quiz(context):
            file_id = document.file_id
            file_name = document.file_name

            # Define where to save the document and download it
            local_file_path = f"downloads/{file_name}"
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            file = await context.bot.get_file(file_id)
            await file.download_to_drive(local_file_path)

            # Extract Text from the file or link
            extracted_text = TextExtractor().extract_text_from_document(local_file_path)
            print(extracted_text)
            if extracted_text:
                # Generate MCQ from the extracted text
                extracted_questions = await TextToMCQ(QuizParameters.get_is_premium(context))\
                                                              .generate_mcq_from_text(extracted_text, QuizParameters.get_question_num(context))
                if extracted_questions:
                    print(extracted_questions)
                    # Send the generated quiz to the Telegram chat
                    await Quiz(extracted_questions).txt_quiz_to_tele_quiz(update, context, QuizParameters.get_question_timer(context))
            os.remove(local_file_path)

    if chat.type == "private":
        db = await global_search("users", "user_id", user.id)
        if db[0] == False:
            await Message.reply_msg(update, db[1])
            return

        find_user = db[1]

        echo_status = find_user.get("echo")
        auto_tr_status = find_user.get("auto_tr")

        if echo_status:
            await Message.reply_msg(update, msg)

        if auto_tr_status:
            lang_code = find_user.get("lang")
            tr_msg = await translate(msg, lang_code)
            if not tr_msg:
                btn_name = ["Language code's"]
                btn_url = ["https://telegra.ph/Language-Code-12-24"]
                btn = await Button.ubutton(btn_name, btn_url)
                await Message.send_msg(chat.id, "Chat language not found/invalid! Use /settings to set your language.",
                                       btn)
                return

            if tr_msg != msg:
                await Message.reply_msg(update, tr_msg)



    elif chat.type in ["group", "supergroup"]:
        _chk_per = await _check_permission(update, user=user, checking_msg=False)
        if not _chk_per:
            return

        _bot_info, bot_permission, user_permission, victim_permission = _chk_per

        if bot_permission.status != ChatMember.ADMINISTRATOR:
            await Message.send_msg(chat.id, "I'm not an admin in this chat!")
            return

        db = await global_search("groups", "chat_id", chat.id)
        if db[0] == False:
            await Message.reply_msg(update, db[1])
            return

        find_group = db[1]

        all_links = find_group.get("all_links")
        allowed_links = find_group.get("allowed_links")

        if not allowed_links:
            allowed_links = []
        else:
            storage = []
            for i in allowed_links:
                storage.append(i.strip())
            allowed_links = storage

        echo_status = find_group.get("echo")
        auto_tr_status = find_group.get("auto_tr")
        lang_code = find_group.get("lang")
        filters = find_group.get("filters")

        msg_contains_link = False

        if all_links:
            if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                links_list = await RE_LINK.detect_link(msg)
                if links_list:
                    clean_msg = msg
                    allowed_links_count = 0
                    for link in links_list:
                        domain = await RE_LINK.get_domain(link)
                        if domain in allowed_links:
                            allowed_links_count += 1
                        else:
                            if all_links == "delete":
                                clean_msg = clean_msg.replace(link, f"<code>forbidden link</code>")
                            if all_links == "convert":
                                b64_link = await BASE64.encode(link)
                                clean_msg = clean_msg.replace(link, f"<code>{b64_link}</code>")
                    if allowed_links_count != len(links_list):
                        try:
                            clean_msg = f"{user.mention_html()}\n\n{clean_msg}\n\n<i>Delete reason: your message contains forbidden link/s!</i>"
                            await Message.del_msg(chat.id, e_msg)
                            await Message.send_msg(chat.id, clean_msg)
                            msg_contains_link = True
                        except Exception as e:
                            logger.error(e)

        if echo_status and not msg_contains_link:
            await Message.reply_msg(update, msg)

        if auto_tr_status:
            to_translate = msg
            if msg_contains_link:
                to_translate = clean_msg
            tr_msg = await translate(to_translate, lang_code)
            if tr_msg != to_translate:
                await Message.reply_msg(update, tr_msg)
            elif not tr_msg:
                logger.error(e)
                btn_name = ["Language code's"]
                btn_url = ["https://telegra.ph/Language-Code-12-24"]
                btn = await Button.ubutton(btn_name, btn_url)
                await Message.send_msg(chat.id, "Chat language not found/invalid! Use /settings to set your language.",
                                       btn)

        if filters:
            for keyword in filters:
                filter_msg = msg.lower() if not isinstance(msg, int) else msg
                if keyword.lower() in filter_msg:
                    filtered_msg = filters[keyword]
                    formattings = {
                        "{first}": user.first_name,
                        "{last}": user.last_name,
                        "{fullname}": user.full_name,
                        "{username}": user.username,
                        "{mention}": user.mention_html(),
                        "{id}": user.id,
                        "{chatname}": chat.title
                    }

                    for key, value in formattings.items():
                        if not value:
                            value = ""
                        filtered_msg = filtered_msg.replace(key, str(value))
                    await Message.reply_msg(update, filtered_msg)
