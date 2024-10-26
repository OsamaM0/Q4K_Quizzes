import time

from bot import logger
from bot.modules.database.mongodb import MongoDB
from bot.modules.database.local_database import LOCAL_DATABASE
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


async def global_search(collection, search, match):
    """
    collection: collection_name\n
    search: eg user_id, chat_id\n
    match: eg. user.id, chat.id\n
    workflow > search on local_db > if not found > search on mongodb > return bool or find_user/find_group = [1]
    """
    if collection == "bot_docs":
        find_db = await LOCAL_DATABASE.find(collection)
        if not find_db:
            find = await MongoDB.find("bot_docs", "_id")
            find_db = await MongoDB.find_one("bot_docs", "_id", find[0])
    else:
        find_db = await LOCAL_DATABASE.find_one(collection, match)
        if not find_db:
            find_db = await MongoDB.find_one(collection, search, match)
            if find_db:
                await LOCAL_DATABASE.insert_data(collection, match, find_db)
    
    if not find_db:
        return False, "⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!"
    else:
        return True, find_db


async def find_bot_docs():
    """
    workflow > search on local_db > if not found > search on mongodb > return error or _bot
    """
    _bot = await LOCAL_DATABASE.find("bot_docs")
    if not _bot:
        find = await MongoDB.find("bot_docs", "_id")
        _bot = await MongoDB.find_one("bot_docs", "_id", find[0])
        if not _bot:
            logger.error("_bot not found in mongodb...")
            return
        await LOCAL_DATABASE.insert_data_direct("bot_docs", _bot)
    return _bot


async def check_add_user_db(user):
    """
    workflow > check local_db for user, if not > check mongodb if not > add data else nothing
    """
    find_user = await LOCAL_DATABASE.find_one("users", user.id)
    if not find_user:
        find_user = await MongoDB.find_one("users", "user_id", user.id)
        subscription_start = datetime.utcnow()
        subscription_end = subscription_start + relativedelta(months=1)
 
        if find_user:
            await LOCAL_DATABASE.insert_data("users", user.id, find_user)
        if not find_user:
            data = {
                "user_id": user.id,
                "Name": user.full_name,
                "username": user.username,
                "mention": user.mention_html(),
                "lang": user.language_code,
                "active_status": True,
                "premium": True,
                "premium_expiration": subscription_end.isoformat(),
                "reminig_premium_quizzes": 100,
            }
            print(data)

            await MongoDB.insert_single_data("users", data)
            await LOCAL_DATABASE.insert_data("users", user.id, data)



async def subscribe_user(user_id, is_premium=False, subscription_days=30, subscription_quizzes=10000):
    """
    Subscribe the user or set the default subscription if no subscription is found.
    - If 'is_premium' is True, the user will get premium for 'subscription_days'.
    - If 'is_premium' is False, the user will be unsubscribed.
    """

    # Check if the user exists in local or MongoDB
    find_user = await LOCAL_DATABASE.find_one("users", user_id)

    if not find_user:
        find_user = await MongoDB.find_one("users", "user_id", user_id)

    # If the user exists, update the subscription status
    if find_user:
        current_date = datetime.utcnow()
        if is_premium:
            # Add premium subscription
            premium_expiration = current_date + timedelta(days=subscription_days)
            update_data = {
                "premium": True,
                "premium_expiration": premium_expiration.isoformat(),
                "reminig_premium_quizzes": subscription_quizzes ,  # Set default quizzes count or any other premium data
            }

        # Update user subscription status in both databases
        await MongoDB.update_one("users", {"user_id": user_id}, {"$set": update_data})
        await LOCAL_DATABASE.update_one("users", {"user_id": user_id}, {"$set": update_data})


    return {"status": "success", "user_id": user_id, "is_premium": is_premium}
