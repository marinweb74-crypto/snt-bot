import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL", "")
NOTIFY_CHAT_ID = int(os.getenv("NOTIFY_CHAT_ID", "0"))
