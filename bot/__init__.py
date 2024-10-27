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


# Function to get environment variable or default
def get_env_variable(var_name, default_value=None):
    value = os.environ[var_name]
    if value is None and default_value is not None:
        logger.warning(f"{var_name} not set, using default: {default_value}")
        return default_value
    elif value is None:
        logger.error(f"Environment variable {var_name} not found and no default provided. Exiting...")
        exit(1)
    return value


# Load environment variables with default fallbacks
bot_token = get_env_variable("BOT_TOKEN")
owner_id = get_env_variable("OWNER_ID", "default_owner_id")
owner_username = get_env_variable("OWNER_USERNAME", "default_owner_username")
bot_pic = get_env_variable("BOT_PIC", "default_bot_pic.jpg")
welcome_img = get_env_variable("WELCOME_IMG", "default_welcome_img.jpg")
github_repo = get_env_variable("GITHUB_REPO", "https://github.com/default/repo")

# Database variables
mongodb_uri = get_env_variable("MONGODB_URI", "mongodb://localhost:27017")
db_name = get_env_variable("DB_NAME", "default_db_name")

# Alive server URL
server_url = get_env_variable("SERVER_URL", "http://localhost:5000")

# API keys
shrinkme_api = get_env_variable("SHRINKME_API", "default_shrinkme_api")
omdb_api = get_env_variable("OMDB_API", "default_omdb_api")
weather_api = get_env_variable("WEATHER_API", "default_weather_api")
pastebin_api = get_env_variable("PASTEBIN_API", "default_pastebin_api")

# Log loaded variables for debugging (exclude sensitive information in production)
logger.info("Loaded environment variables and configuration.")

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
