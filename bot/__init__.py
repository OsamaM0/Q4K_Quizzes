import json
from telegram import Bot
from bot.alive import alive
import os
import logging
from dotenv import load_dotenv

# Enable logging
logging.basicConfig(
    filename="log.txt",
    format="%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(filename)s - %(message)s",
    level=logging.INFO
)

# Set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

# Console logging configuration
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(filename)s - %(message)s")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)

logger = logging.getLogger(__name__)

# Load environment configuration
config_file = load_dotenv("config.env")
if not config_file:
    logger.error("config.env not found...\nExiting...")
    exit(1)

# Load environment variables
bot_token = os.getenv("BOT_TOKEN")
owner_id = os.getenv("OWNER_ID")
owner_username = os.getenv("OWNER_USERNAME")
bot_pic = os.getenv("BOT_PIC")
welcome_img = os.getenv("WELCOME_IMG")
github_repo = os.getenv("GITHUB_REPO")

# Database variables
mongodb_uri = os.getenv("MONGODB_URI")
db_name = os.getenv("DB_NAME")

# Alive server URL
server_url = os.getenv("SERVER_URL")

# API keys
shrinkme_api = os.getenv("SHRINKME_API")
omdb_api = os.getenv("OMDB_API")
weather_api = os.getenv("WEATHER_API")
pastebin_api = os.getenv("PASTEBIN_API")

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
