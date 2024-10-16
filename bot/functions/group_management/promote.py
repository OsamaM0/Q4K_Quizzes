from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot import bot, logger
from bot.helper.telegram_helper import Message
from bot.functions.group_management.pm_error import _pm_error
from bot.functions.admin.del_command import func_del_command
from bot.functions.group_management.check_permission import _check_permission


async def func_promote(update: Update, context: ContextTypes.DEFAULT_TYPE, is_silent=bool(None), full_promote=bool(None), is_anonymous=bool(None)):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    victim = reply.from_user if reply else None
    admin_title = " ".join(context.args)
    
    if chat.type not in ["group", "supergroup"]:
        await _pm_error(chat.id)
        return
    
    await func_del_command(update, context)

    if user.is_bot:
        await Message.reply_msg(update, "I don't take permission from anonymous admins!")
        return

    _chk_per = await _check_permission(update, victim, user)

    if not _chk_per:
        return
    
    _bot_info, bot_permission, user_permission, victim_permission = _chk_per

    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this chat!")
        return
    
    if not bot_permission.can_promote_members:
        await Message.reply_msg(update, "I don't have enough rights to promote/demote chat member!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin in this chat!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not user_permission.can_promote_members:
            await Message.reply_msg(update, "You don't have enough rights to promote/demote chat member!")
            return
    
    if not reply:
        await Message.reply_msg(update, "I don't know who you are talking about! Reply the member whom you want to promote!\nTo set admin_title eg. <code>/promote admin_title</code>")
        return
    
    if victim_permission.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        if _bot_info.id == victim.id:
            await Message.reply_msg(update, "I'm already an admin!")
        else:
            await Message.reply_msg(update, "The user is already an admin!")
        return
    
    try:
        if full_promote:
            await bot.promote_chat_member(
                chat.id,
                victim.id,
                can_change_info = True,
                can_delete_messages = True,
                can_invite_users = True,
                can_restrict_members = True,
                can_pin_messages = True,
                can_promote_members = True,
                is_anonymous = is_anonymous,
                can_manage_chat = True,
                can_manage_video_chats = True,
                can_post_stories = True,
                can_edit_stories = True,
                can_delete_stories = True
            )
            msg = f"{victim.mention_html()} has been promoted (with full privilege)!\n<b>Admin</b>: {user.first_name}"
        else:
            await bot.promote_chat_member(chat.id, victim.id, can_manage_video_chats=True, is_anonymous=is_anonymous)
            msg = f"{victim.mention_html()} has been promoted!\n<b>Admin</b>: {user.first_name}"
    except Exception as e:
        logger.error(e)
        error_msg = await Message.reply_msg(update, e)
        if not error_msg:
            await Message.reply_msg(update, e.message)
        return
    
    if admin_title:
        try:
            await bot.set_chat_administrator_custom_title(chat.id, victim.id, admin_title)
            msg = f"{msg}\nNew admin title: {admin_title}"
        except Exception as e:
            logger.error(e)
            error_msg = await Message.reply_msg(update, e)
            if not error_msg:
                await Message.reply_msg(update, e.message)
    
    if not is_silent:
        await Message.reply_msg(update, msg)


async def func_apromote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await func_promote(update, context, is_anonymous=True)


async def func_spromote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    e_msg = update.effective_message
    
    await Message.del_msg(chat.id, e_msg)
    await func_promote(update, context, is_silent=True)


async def func_sapromote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    e_msg = update.effective_message
    
    await Message.del_msg(chat.id, e_msg)
    await func_promote(update, context, is_silent=True, is_anonymous=True)


async def func_fpromote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await func_promote(update, context, full_promote=True)


async def func_fapromote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await func_promote(update, context, full_promote=True, is_anonymous=True)


async def func_sfpromote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    e_msg = update.effective_message

    await Message.del_msg(chat.id, e_msg)
    await func_promote(update, context, is_silent=True, full_promote=True)


async def func_sfapromote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    e_msg = update.effective_message

    await Message.del_msg(chat.id, e_msg)
    await func_promote(update, context, is_silent=True, full_promote=True, is_anonymous=True)
