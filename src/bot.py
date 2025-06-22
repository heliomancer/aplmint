# src/bot.py
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

# Import our own modules
from . import config
from . import database
from . import handlers

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

def main() -> None:
    """Sets up and runs the Telegram bot."""
    # Initialize the database
    database.init_db()

    # Create the Telegram Application using the token from our config
    application = Application.builder().token(config.TELEGRAM_TOKEN).build()

    # Register the handlers from the handlers.py file
    application.add_handler(CommandHandler("start", handlers.start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.message_handler))
    application.add_handler(CommandHandler("model", handlers.model_select_menu))
    application.add_handler(CallbackQueryHandler(handlers.model_button_callback, pattern="^model_"))

    # Start the bot
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
