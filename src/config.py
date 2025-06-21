import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") 

if not TELEGRAM_TOKEN:
    raise ValueError("Secrets like TELEGRAM_BOT_TOKEN are not set!")