import os
import json
import logging
from telegram import Bot
from dotenv import load_dotenv
from bot.alive import alive

open('log.txt', 'w')

#Enable logging
logging.basicConfig(
    filename="log.txt", format="%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(filename)s - %(message)s", level=logging.INFO
)
#set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(filename)s - %(message)s")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)

logger = logging.getLogger(__name__)

config_file = load_dotenv("config.env")
# if not config_file:
#     logger.error("config.env not found...\nExiting...")
#     exit(1)

# bot_token = os.getenv("BOT_TOKEN")
# owner_id = os.getenv("OWNER_ID")
# owner_username = os.getenv("OWNER_USERNAME")
# bot_pic = os.getenv("BOT_PIC")
# welcome_img = os.getenv("WELCOME_IMG")
# github_repo = os.getenv("GITHUB_REPO")
# #database
# mongodb_uri = os.getenv("MONGODB_URI")
# db_name = os.getenv("DB_NAME")
# #alive
# server_url = os.getenv("SERVER_URL")
# #api's
# shrinkme_api = os.getenv("SHRINKME_API")
# omdb_api = os.getenv("OMDB_API")
# weather_api = os.getenv("WEATHER_API")
# pastebin_api = os.getenv("PASTEBIN_API")


bot_token = "7185784676:AAHZPU-liQnJ4yUGlDDs_JWQ9vFvd6RrK98"
owner_id = "5549398282"
owner_username = "osama_mo7"
bot_pic = "https://mostaql.hsoubcdn.com/uploads/thumbnails/2272598/6456b5b02b905/Q4K-MCQ-Telegram-Bot.jpg"
welcome_img = "https://mostaql.hsoubcdn.com/uploads/thumbnails/2272598/6456b5b02b905/Q4K-MCQ-Telegram-Bot.jpg"
github_repo = "https://github.com/OsamaM0"
#database
mongodb_uri = "mongodb+srv://osamamoabd1:5BxxHzbLz7L3j7eg@q4kquizess.ahqjo.mongodb.net/?retryWrites=true&w=majority&appName=Q4KQUIZESS"
db_name = "Q4KQuizzes"
#alive
server_url = "https://q4kquizess.herokuapp.com/"
#api's
shrinkme_api = "5deb9a31aed28b679046d4bb5ddbaf845678c3be"                     # STR Get from > https://shrinkme.io/
omdb_api = "a9fabfe8"                         # STR Get from > https://www.omdbapi.com/
weather_api = "c8c565323b6c441cb08103240243108"                      # STR Get from > https://www.weatherapi.com/
pastebin_api = "DPlsl8Dii4cp7iTOcQMAdXiatSCeKxLK"                     # STR Get from > https://pastebin.com/doc_api

#psndl
psndl_db = "https://raw.githubusercontent.com/bishalqx980/python/main/psndl%20(ps3)/psndl_db.json"

variables = [bot_token, mongodb_uri, db_name]
for variable in variables:
    if len(variable) == 0:
        logger.error(f"Check config.env again... [some value are empty]")
        exit(1)
    else:
        pass

LOCAL_DB = "database.json"

check_local_db = os.path.isfile(LOCAL_DB)
if not check_local_db:
    logger.info("localdb not found...")
    json.dump({}, open(LOCAL_DB, "w"))
    logger.info("localdb created...")

try:
    json.dump(
        {"bot_docs": {}, "_bot_info": {}, "users": {}, "groups": {}, "data_center": {}},
        open(LOCAL_DB, "w"),
        indent=4
    )
    logger.info("localdb updated...")
except Exception as e:
    logger.error(e)

bot = Bot(bot_token)

logger.info(
'''
Developed by


░█████╗░░██████╗░█████╗░███╗░░░███╗░█████╗░  ███╗░░░███╗░█████╗░
██╔══██╗██╔════╝██╔══██╗████╗░████║██╔══██╗  ████╗░████║██╔══██╗
██║░░██║╚█████╗░███████║██╔████╔██║███████║  ██╔████╔██║██║░░██║
██║░░██║░╚═══██╗██╔══██║██║╚██╔╝██║██╔══██║  ██║╚██╔╝██║██║░░██║
╚█████╔╝██████╔╝██║░░██║██║░╚═╝░██║██║░░██║  ██║░╚═╝░██║╚█████╔╝
░╚════╝░╚═════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝  ╚═╝░░░░░╚═╝░╚════╝░      
                            Library python-telegram-bot

'''
)

alive()
