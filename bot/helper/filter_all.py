from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot import logger
from bot.helper.telegram_helper import Message, Button, Quiz
from bot.modules.database.combined_db import global_search
from bot.modules.database.local_database import LOCAL_DATABASE
from bot.modules.quizzes.quizz_parameters import QuizParameters
from bot.modules.quizzes.quiz_database import QuizDataHandler
from bot.modules.translator import translate
from bot.functions.group_management.check_permission import _check_permission
from bot.modules.re_link import RE_LINK
from bot.modules.base64 import BASE64
from bot.modules.text_extractor.text_extractor import TextExtractor
from bot.modules.mcq_generator.text_to_mcq_manager import TextToMCQ
from bot.functions.quizzes.quizzes import handle_quiz_request
from bot.modules.ai.ai_modules import AIModules
from bot.helper.telegram_helper import Message
from docx import Document
import os
from bot.modules.ytdl import PYTUBE
from bot.modules.subs.subs_manger import SubsManager


async def func_filter_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # previous_msg = await Message.get_previous_message(update, context)
    # print(previous_msg)
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message
    msg = update.message.text_html or update.message.caption_html if update.message else None
    document = update.message.document
    # video = update.message.video

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

            for key, value in zip([
                    "edit_data_value", "edit_data_value_msg_pointer_id",
                    "is_editing"
            ], [msg, e_msg.id, False]):
                await LOCAL_DATABASE.insert_data("data_center", chat.id,
                                                 {key: value})
            return

    # Hanlde Quiz Part Workflow
    if QuizParameters.get_mode(context):
        local_file_path = None
        extracted_text = None
        is_youtube_link = False
        is_sanfroundry_link = False
        
        if msg:
            # Check if message is a link
            domain = await RE_LINK.get_domain(msg)
            # Check if message parameter of quiz
            if (not domain ) and QuizParameters.is_quiz_mode(context):
                print("START HANDLE QUIZ")
                await handle_quiz_request(update, context)
                return

        if QuizParameters.is_premium_quiz_mode(context) and not QuizParameters.get_question_num(context):
            sent_msg = await Message.reply_msg(
                update, "Please send valid digit number <b>to reprsent number of questions will be Generate</b>.\nEx. <blockquote><code>n=5</code></blockquote>")
            return
            
        # If a document is sent
        if document:
            sent_msg = await Message.reply_msg(
                update, "📜 Extracting Text from the Document...")

            file_id = document.file_id
            file_name = document.file_name

            # Define where to save the document and download it
            local_file_path = f"download/{file_name}"
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            file = await context.bot.get_file(file_id)
            await file.download_to_drive(local_file_path)

        elif domain in ["youtube.com", "youtu.be"]:
            is_youtube_link = True
            file_name = "Youtube Video"
            sent_msg = await Message.reply_msg(update, "🎥 Extracting Text from YouTube Video...")
            
            # Check if the youtube subtitles text in the database
            extracted_text = await QuizDataHandler().get_youtube_entry(msg)
            extracted_text = extracted_text.get("text", None)
            
            if not extracted_text:
                # Extract Subtitles from youtube link
                extracted_text = await PYTUBE.get_subtitles(msg)
                
                if not extracted_text:
                    if not extracted_text:
                        logger.info(
                            "No subtitles found, attempting Speech-to-Text (STT)...")
                        
                        # Download audio if no subtitles are found
                        is_downloaded, local_file_path = await PYTUBE.ytdl(msg, extention="mp3")
                        if not is_downloaded:
                            await Message.edit_msg(update, f"❌ Failed to download the audio file, please try again later.", sent_msg)
                    
        elif domain == "www.sanfoundry":
            sent_msg = await Message.reply_msg(
                update, "🔗 Extracting Text from the Link...")
            is_sanfroundry_link = True
            local_file_path = msg


        # Extract Text from the file
        if local_file_path:
            extracted_text = await TextExtractor().extract_text_from_document(local_file_path)
            if not is_sanfroundry_link:
                os.remove(local_file_path)

        if extracted_text:
            subs_manager = SubsManager(user.id)

            # Save extracted text to database
            if QuizParameters.is_quiz_mode(context):
                # Validate user subscription and coin balance using SubsManager
                is_premium_active, remaining_coins = await subs_manager.validate_user_subscription(update, "quiz", context)
                if not is_premium_active:
                    return
                
                await Message.edit_msg(update, "📤 Generating Questions...", sent_msg)
                # Generate MCQ from the extracted text
                extracted_questions = await TextToMCQ(context)\
                                                              .generate_mcq_from_text(msg, extracted_text, QuizParameters.get_question_num(context))
                if extracted_questions:
                    # Send the generated quiz to the Telegram chat
                    sended_q = await Quiz(extracted_questions).txt_quiz_to_tele_quiz(
                                                                                    update, context,
                                                                                    QuizParameters.get_question_timer(context))
                    end_msg = f"Quiz questions generated! You received {sended_q} Question(s)"
                    if QuizParameters.is_premium_quiz_mode(context):
                        # Update user question number sended
                        await subs_manager.use_coins(sended_q)
                        # Send complate message to user
                        coins = await subs_manager.get_remaining_coins()
                        msg +=f"<i><b>Coins Remaining</b>: <code>{coins} Coins 🪙</code></i>"

                    await Message.send_msg(chat.id, end_msg)

                    await Message.del_msg(chat.id, sent_msg)


            elif QuizParameters.is_summarize_mode(context):
                # Validate user subscription and coin balance using SubsManager
                is_premium_active, remaining_coins = await subs_manager.validate_user_subscription(update, "summary", context)
                if not is_premium_active:
                    return

                
                await Message.edit_msg(update, "📤 Generating Summarization...",
                                       sent_msg)
                ai_modules = AIModules()
                summarized_text = await ai_modules.generate_summary(extracted_text)

                if summarized_text:
                    
                    coins = await subs_manager.get_remaining_coins()
                    file_path = os.path.join('download', f'summarized_{file_name}_{user.id}.txt')
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    # Add text to the document
                    with open(file_path, "w") as file:
                        file.write(summarized_text["text"])
                    
                    # update coins of subs user
                    await subs_manager.use_summarization()
                    # Send complate message and document to user
                    coins = await subs_manager.get_remaining_coins()
                    await context.bot.send_document(
                        chat.id,
                        document=open(file_path, 'rb'),
                        caption=f"Your Summarization 🤖⚡\nCoins Remaining: {coins} Coins 🪙")
                    
                    # update user text 
                    await QuizDataHandler().add_entry(msg if is_youtube_link else local_file_path, extracted_text, summarization=summarized_text["text"]) 

                    await Message.del_msg(chat.id, sent_msg)
                    os.remove(file_path)

            

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
                btn_url = ["https://telegra.ph/Language-Code-Q4K-10-23"]
                btn = await Button.ubutton(btn_name, btn_url, update= update)
                await Message.send_msg(
                    chat.id,
                    "Chat language not found/invalid! Use /settings to set your language.",
                    btn)
                return

            if tr_msg != msg:
                await Message.reply_msg(update, tr_msg)

    elif chat.type in ["group", "supergroup"]:
        _chk_per = await _check_permission(update,
                                           user=user,
                                           checking_msg=False)
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
            if user_permission.status not in [
                    ChatMember.ADMINISTRATOR, ChatMember.OWNER
            ]:
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
                                clean_msg = clean_msg.replace(
                                    link, f"<code>forbidden link</code>")
                            if all_links == "convert":
                                b64_link = await BASE64.encode(link)
                                clean_msg = clean_msg.replace(
                                    link, f"<code>{b64_link}</code>")
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
                btn_url = ["https://telegra.ph/Language-Code-Q4K-10-23"]
                btn = await Button.ubutton(btn_name, btn_url, update= update)
                await Message.send_msg(
                    chat.id,
                    "Chat language not found/invalid! Use /settings to set your language.",
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
