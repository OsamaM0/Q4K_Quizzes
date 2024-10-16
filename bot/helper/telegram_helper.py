import telegram
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, Poll
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from telegram.error import Forbidden
from bot import bot, logger
import random


class Message:

    async def send_msg(chat_id,
                       msg,
                       btn=None,
                       parse_mode=ParseMode.HTML,
                       disable_web_preview=True):
        if btn:
            try:
                reply_markup = InlineKeyboardMarkup(btn)
                response = await bot.send_message(
                    chat_id=chat_id,
                    text=msg,
                    reply_markup=reply_markup,
                    disable_web_page_preview=bool(disable_web_preview),
                    parse_mode=parse_mode)
                return response
            except Forbidden:
                return Forbidden
            except Exception as e:
                logger.error(e)
        else:
            try:
                response = await bot.send_message(
                    chat_id=chat_id,
                    text=msg,
                    disable_web_page_preview=bool(disable_web_preview),
                    parse_mode=parse_mode)
                return response
            except Forbidden:
                return Forbidden
            except Exception as e:
                logger.error(e)

    async def send_img(chat_id,
                       img,
                       caption=None,
                       btn=None,
                       parse_mode=ParseMode.HTML):
        if btn:
            try:
                reply_markup = InlineKeyboardMarkup(btn)
                response = await bot.send_photo(chat_id=chat_id,
                                                photo=img,
                                                caption=caption,
                                                reply_markup=reply_markup,
                                                parse_mode=parse_mode)
                return response
            except Forbidden:
                return Forbidden
            except Exception as e:
                logger.error(e)
        else:
            try:
                response = await bot.send_photo(chat_id=chat_id,
                                                photo=img,
                                                caption=caption,
                                                parse_mode=parse_mode)
                return response
            except Forbidden:
                return Forbidden
            except Exception as e:
                logger.error(e)

    async def send_vid(chat_id,
                       video,
                       thumbnail=None,
                       caption=None,
                       reply_msg_id=None,
                       btn=None,
                       parse_mode=ParseMode.HTML):
        if btn:
            try:
                reply_markup = InlineKeyboardMarkup(btn)
                response = await bot.send_video(
                    chat_id=chat_id,
                    video=video,
                    caption=caption,
                    reply_to_message_id=reply_msg_id,
                    reply_markup=reply_markup,
                    thumbnail=thumbnail,
                    height=1080,
                    width=1920,
                    supports_streaming=True,
                    parse_mode=parse_mode)
                return response
            except Forbidden:
                return Forbidden
            except Exception as e:
                logger.error(e)
        else:
            try:
                response = await bot.send_video(
                    chat_id=chat_id,
                    video=video,
                    caption=caption,
                    reply_to_message_id=reply_msg_id,
                    thumbnail=thumbnail,
                    height=1080,
                    width=1920,
                    supports_streaming=True,
                    parse_mode=parse_mode)
                return response
            except Forbidden:
                return Forbidden
            except Exception as e:
                logger.error(e)

    async def send_audio(chat_id,
                         audio,
                         title,
                         caption=None,
                         reply_msg_id=None,
                         parse_mode=ParseMode.HTML):
        try:
            response = await bot.send_audio(chat_id=chat_id,
                                            audio=audio,
                                            title=title,
                                            caption=caption,
                                            reply_to_message_id=reply_msg_id,
                                            parse_mode=parse_mode)
            return response
        except Forbidden:
            return Forbidden
        except Exception as e:
            logger.error(e)

    async def send_doc(chat_id,
                       doc,
                       filename,
                       caption=None,
                       reply_msg_id=None,
                       parse_mode=ParseMode.HTML):
        """
        doc = send as file > with open()
        """
        try:
            response = await bot.send_document(
                chat_id=chat_id,
                document=doc,
                filename=filename,
                caption=caption,
                reply_to_message_id=reply_msg_id,
                parse_mode=parse_mode)
            return response
        except Forbidden:
            return Forbidden
        except Exception as e:
            logger.error(e)

    async def reply_msg(update: Update,
                        msg,
                        btn=None,
                        parse_mode=ParseMode.HTML,
                        disable_web_preview=True):
        chat = update.effective_chat
        e_msg = update.effective_message
        re_msg = e_msg.reply_to_message
        msg_id = re_msg.message_id if re_msg else e_msg.message_id

        if btn:
            reply_markup = InlineKeyboardMarkup(btn)
            try:
                response = await update.message.reply_text(
                    text=msg,
                    disable_web_page_preview=bool(disable_web_preview),
                    reply_to_message_id=msg_id,
                    reply_markup=reply_markup,
                    parse_mode=parse_mode)
                return response
            except Forbidden:
                return Forbidden
            except Exception as e:
                logger.error(e)
                try:
                    reply_markup = InlineKeyboardMarkup(btn)
                    response = await bot.send_message(
                        chat_id=chat.id,
                        text=msg,
                        reply_markup=reply_markup,
                        disable_web_page_preview=bool(disable_web_preview),
                        parse_mode=parse_mode)
                    return response
                except Forbidden:
                    return Forbidden
                except Exception as e:
                    logger.error(e)
        else:
            try:
                response = await update.message.reply_text(
                    text=msg,
                    disable_web_page_preview=bool(disable_web_preview),
                    reply_to_message_id=msg_id,
                    parse_mode=parse_mode)
                return response
            except Forbidden:
                return Forbidden
            except Exception as e:
                logger.error(e)
                try:
                    response = await bot.send_message(
                        chat_id=chat.id,
                        text=msg,
                        disable_web_page_preview=bool(disable_web_preview),
                        parse_mode=parse_mode)
                    return response
                except Forbidden:
                    return Forbidden
                except Exception as e:
                    logger.error(e)

    async def forward_msg(chat_id, from_chat_id, msg_id):
        """
        chat_id > where you want to send\n
        from_chat_id > effective chat id\n
        msg_id > effective message id
        """
        try:
            response = await bot.forward_message(chat_id=chat_id,
                                                 from_chat_id=from_chat_id,
                                                 message_id=msg_id)
            return response
        except Forbidden:
            return Forbidden
        except Exception as e:
            logger.error(e)

    async def edit_msg(update: Update,
                       edit_msg_text,
                       sent_msg_pointer,
                       btn=None,
                       parse_mode=ParseMode.HTML,
                       disable_web_preview=True):
        caption_msg = sent_msg_pointer.caption
        chat_id = update.effective_chat.id
        msg_id = sent_msg_pointer.message_id

        if caption_msg and btn:
            try:
                reply_markup = InlineKeyboardMarkup(btn)
                response = await bot.edit_message_caption(
                    caption=edit_msg_text,
                    chat_id=chat_id,
                    message_id=msg_id,
                    reply_markup=reply_markup,
                    parse_mode=parse_mode)
                return response
            except Forbidden:
                return Forbidden
            except Exception as e:
                logger.error(e)
        elif caption_msg and not btn:
            try:
                response = await bot.edit_message_caption(
                    caption=edit_msg_text,
                    chat_id=chat_id,
                    message_id=msg_id,
                    parse_mode=parse_mode)
                return response
            except Forbidden:
                return Forbidden
            except Exception as e:
                logger.error(e)
        elif not caption_msg and btn:
            try:
                reply_markup = InlineKeyboardMarkup(btn)
                response = await bot.edit_message_text(
                    text=edit_msg_text,
                    chat_id=chat_id,
                    message_id=msg_id,
                    reply_markup=reply_markup,
                    disable_web_page_preview=bool(disable_web_preview),
                    parse_mode=parse_mode)
                return response
            except Forbidden:
                return Forbidden
            except Exception as e:
                logger.error(e)
        elif not caption_msg and not btn:
            try:
                response = await bot.edit_message_text(
                    text=edit_msg_text,
                    chat_id=chat_id,
                    message_id=msg_id,
                    disable_web_page_preview=bool(disable_web_preview),
                    parse_mode=parse_mode)
                return response
            except Forbidden:
                return Forbidden
            except Exception as e:
                logger.error(e)

    async def del_msg(chat_id, msg_pointer=None, msg_id=None):
        if not msg_pointer and not msg_id:
            logger.error("msg_pointer or msg_id not specified!")
            return

        msg_id = msg_pointer.message_id if msg_pointer else msg_id
        try:
            response = await bot.delete_message(chat_id=chat_id,
                                                message_id=msg_id)
            return response
        except Forbidden:
            return Forbidden
        except Exception as e:
            logger.error(e)


class Button:

    async def ubutton(btn_name, url, same_line=bool(False)):
        """
        Example usage:\n
        btn_name = ["Google"]\n
        url = ["https://google.com"]\n
        btn = await Button.ubutton(btn_name, url)\n\n
        -> for multiple row\n
        btn_name_1 = ["Google", "Bing"]\n
        url_1 = ["https://google.com", "https://bing.com"]\n
        btn_name_2 = ["Facebook", "X (Twitter)"]\n
        url_2 = ["https://facebook.com", "https://x.com"]\n\n
        row1 = await Button.ubutton(btn_name_1, url_1, True) # 1st line and both button are in same line\n
        row2 = await Button.ubutton(btn_name_1, url_1) # 2nd line (facebook) and 3rd line (x) becasue not in same line\n\n
        btn = row1 + row 2\n
        """
        btn = []
        sbtn = []

        if len(btn_name) != len(url):
            logger.error(
                f"btn={len(btn_name)} not equal url={len(url)}! Skiping...")
            return

        try:
            for b_name, url_link in zip(
                    btn_name, url
            ):  # list1 = [1, 2, 3] list2 = ['a', 'b'] Output: [(1, 'a'), (2, 'b')]
                if same_line:
                    sbtn.append(InlineKeyboardButton(b_name, url_link))
                else:
                    btn.append([InlineKeyboardButton(b_name, url_link)])
            buttons = btn + [sbtn]
            return buttons
        except Exception as e:
            logger.error(e)

    async def cbutton(btn_name, callback_name, same_line=bool(False)):
        """
        Example usage:\n
        btn_name = ["Google"]\n
        callback_name = ["data"]\n
        btn = await Button.cbutton(btn_name, callback_name)\n\n
        -> for multiple row\n
        btn_name_1 = ["Google", "Bing"]\n
        callback_name_1 = ["google", "bing"]\n
        btn_name_2 = ["Facebook", "X (Twitter)"]\n
        callback_name_2 = ["facebook", "x_twitter"]\n\n
        row1 = await Button.cbutton(btn_name_1, callback_name_1, True) # 1st line and both button are in same line\n
        row2 = await Button.cbutton(btn_name_1, callback_name_2) # 2nd line (facebook) and 3rd line (x) becasue not in same line\n\n
        btn = row1 + row 2
        """
        btn = []
        sbtn = []

        if len(btn_name) != len(callback_name):
            logger.error(
                f"Error: btn={len(btn_name)} not equal callback={len(callback_name)}! Skiping..."
            )
            return

        try:
            for b_name, c_name in zip(
                    btn_name, callback_name
            ):  # list1 = [1, 2, 3] list2 = ['a', 'b'] Output: [(1, 'a'), (2, 'b')]
                if same_line:
                    sbtn.append(
                        InlineKeyboardButton(b_name, callback_data=c_name))
                else:
                    btn.append(
                        [InlineKeyboardButton(b_name, callback_data=c_name)])
            buttons = btn + [sbtn]
            return buttons
        except Exception as e:
            logger.error(e)


class Quiz:
    def __init__(self, questions):
        """Initialize the Quiz with a list of questions."""
        self.questions = questions

    async def add_quiz_question(self, update, context, quiz_question, explanation, period=None):
        """Send a quiz question as a poll message."""
        try:
            message = await context.bot.send_poll(
                chat_id=update.effective_chat.id,
                question=quiz_question.question,
                options=quiz_question.answers,
                type=Poll.QUIZ,
                correct_option_id=quiz_question.correct_answer_position,
                open_period=period,
                is_anonymous=True,
                explanation=explanation,
                explanation_parse_mode=ParseMode.MARKDOWN_V2,

            )

            # Save poll info to bot_data for later use in answer processing
            context.bot_data.update({message.poll.id: message.chat.id})
        except Exception as e:
            print(f"Error sending quiz question: {e}")

    async def txt_quiz_to_tele_quiz(self, update, context, number, period):
        """Activate quiz mode and send the requested number of quiz questions."""
        if number != 0:
            number = int(number)
            period = int(period) * 60  # Convert minutes to seconds
            number = min(number, len(self.questions))

            # Shuffle the questions to randomize the quiz
            random.shuffle(self.questions)
            questions_to_send = self.questions[:number]

            for question in questions_to_send:
                try:
                    quiz_question = QuizQuestion(
                        question["question"],
                        question["options"],
                        question["answer"]
                    )
                    explanation = question.get("explanation", "No explanation provided.")
                    await self.add_quiz_question(update, context, quiz_question, explanation, period)

                    for l_que in question.get("long_question", []):
                        try:
                            await Message.send_msg(update.effective_chat.id, l_que)
                        except Exception as e:
                            print(f"Error sending audio: {e}")

                    for img_link in question.get("images", []):
                        try:
                            await Message.send_img(update.effective_chat.id, img_link)
                        except Exception as e:
                            print(f"Error sending image: {e}")

                except Exception as e:
                    print(f"Error processing question: {e}")

    def expertise(self, additional_questions):
        """Enhance the quiz by adding more questions dynamically."""
        self.questions.extend(additional_questions)
        random.shuffle(self.questions)  # Shuffle to keep the quiz dynamic

    def filter_questions(self, difficulty_level):
        """Filter quiz questions by difficulty level or any other attribute."""
        return [q for q in self.questions if q.get("difficulty") == difficulty_level]


class QuizQuestion:

    def __init__(self, question="", answers=[], correct_answer=""):
        self.question = question
        self.answers = answers
        self.correct_answer = correct_answer
        self.correct_answer_position = self.__get_correct_answer_position__()

    def __get_correct_answer_position__(self):
        ret = -1

        i = 0
        for answer in self.answers:
            if answer.lower() == self.correct_answer.lower():
                ret = i
                break
            i = i + 1

        return ret

    def __str__(self):
        return f"question:{self.question} answers:{self.answers} correct_answer:{self.correct_answer} correct_answer_position:{self.correct_answer_position} "
