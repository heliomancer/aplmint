import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# DS_API_KEY = os.getenv("DS_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not TELEGRAM_TOKEN or not OPENROUTER_API_KEY:
    raise ValueError("Access tokens are not set!")