from telegram import Update
from bot import bot
from bot.helper.telegram_helper import Message, Button

class QueryGroup:
    async def _query_group_student_management(update: Update, query):
      msg = (
          "🧑‍🎓 <b>Student Management</b>\n"
          "<i>Take control of the students in your group with these powerful commands.</i>\n\n"
          "<blockquote>/id\nRetrieve chat/student ID.</blockquote>\n"
          "<blockquote>/promote | /fpromote\nPromote a student, 'f' for full privileges.</blockquote>\n"
          "<blockquote>/apromote | /fapromote\nPromote anonymously with or without full privilege.</blockquote>\n"
          "<blockquote>/demote\nDemote a student from their role.</blockquote>\n"
          "<blockquote>/ban\nBan a troublesome student from the group.</blockquote>\n"
          "<blockquote>/unban\nUnban a previously banned student.</blockquote>\n"
          "<blockquote>/kick\nRemove a student from the group.</blockquote>\n"
          "<blockquote>/kickme\nLeave the group on your own.</blockquote>\n"
          "<blockquote>/mute\nMute a student, preventing them from sending messages.</blockquote>\n"
          "<blockquote>/unmute\nUnmute a previously muted student.</blockquote>\n"
      )

      btn_name_row1 = ["👥 Group", "📨 Message"]
      btn_data_row1 = ["query_group_group_management", "query_group_message_management"]

      btn_name_row2 = ["Back", "Close"]
      btn_data_row2 = ["query_help_group_management", "query_close"]

      row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True, update= update)
      row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True, update= update)

      btn = row1 + row2

      await Message.edit_msg(update, msg, query.message, btn)


    async def _query_group_group_management(update: Update, query):
        msg = (
            "👥 <b>Group Management</b>\n"
            "<i>Managing your group has never been easier!</i>\n\n"
            "<blockquote>/invite\nGenerate a group invite link.</blockquote>\n"
            "<blockquote>/adminlist\nView the list of current admins.</blockquote>\n"
            "<blockquote>/settings\nAdjust group settings.</blockquote>\n"
            "<blockquote>/lock\nLock the group to restrict activity.</blockquote>\n"
            "<blockquote>/unlock\nUnlock the group to restore activity.</blockquote>\n"
        )

        btn_name_row1 = ["🧑‍🎓 Student", "📨 Message"]
        btn_data_row1 = ["query_group_student_management", "query_group_message_management"]

        btn_name_row2 = ["🔙 Back", "✖️ Close"]
        btn_data_row2 = ["query_help_group_management", "query_close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True, update= update)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True, update= update)

        btn = row1 + row2

        await Message.edit_msg(update, msg, query.message, btn)

    async def _query_group_message_management(update: Update, query):
        msg = (
            "💬 <b>Message Management</b>\n"
            "<i>Keep your chat clean and organized with these message commands.</i>\n\n"
            "<blockquote>/pin\nPin a message with notification.</blockquote>\n"
            "<blockquote>/unpin\nUnpin the current pinned message.</blockquote>\n"
            "<blockquote>/unpinall\nUnpin all pinned messages.</blockquote>\n"
            "<blockquote>/del\nDelete a message with a warning.</blockquote>\n"
            "<blockquote>/purge\nPurge all messages from the replied message to the current one.</blockquote>\n"
            "<blockquote>/filters | /filter | /remove\nManage custom message filters.</blockquote>\n"
        )

        btn_name_row1 = ["👥 Group", "🧑‍🎓 Student"]
        btn_data_row1 = ["query_group_group_management", "query_group_student_management"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["query_help_group_management", "query_close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True, update= update)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True, update= update)

        btn = row1 + row2

        await Message.edit_msg(update, msg, query.message, btn)
