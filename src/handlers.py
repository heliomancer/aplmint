import logging
import asyncio
from telegram import Update
from telegram.ext import ContextTypes

from . import database
# +
# from . import llm_service

logger = logging.getLogger(__name__)

# --- Concurrency Lock ---
# A set to hold the user_ids of users currently waiting for an LLM response.
PROCESSING_USERS = set()

# --- Rate Limit ---
DAILY_QUERY_LIMIT = 10

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hello {user.mention_html()}, I can process your queries for LLM. Just send your text to me. Remember, you have {DAILY_QUERY_LIMIT} queries per day.",
    )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    The main handler with rate limiting and concurrency control.
    """
    user = update.effective_user
    
    # 1. --- RATE LIMIT CHECK ---
    query_count = database.get_user_query_count_today(user.id)
    if query_count >= DAILY_QUERY_LIMIT:
        logger.warning(f"User {user.id} ({user.username}) has reached their daily limit.")
        await update.message.reply_text("You have reached your daily limit of 10 queries. Please try again tomorrow.")
        return

    # 2. --- CONCURRENCY CHECK ---
    if user.id in PROCESSING_USERS:
        logger.info(f"User {user.id} ({user.username}) tried to send a query while another was processing.")
        await update.message.reply_text("I'm still working on your previous request. Please wait a moment!")
        return

    # 3. --- LOCK AND PROCESS ---


    try:
        # Add user to the processing set to "lock" them.
        PROCESSING_USERS.add(user.id)

        message_text = update.message.text
        chat_id = update.message.chat_id

        # Show "typing..." status in Telegram
        await context.bot.send_chat_action(chat_id=chat_id, action='typing')
        
        # Make the expensive API call
        #llm_response = await llm_service.get_llm_response(message_text)

        # Send the response
        #await update.message.reply_text(llm_response)

        ### TEST BLOCK
        # The placeholder response
        response_text = (
            f"Echo: '{message_text}'\n\n"
            "(Note: LLM service is in development. This is a placeholder response.)"
        )

        # simulate the LLM work
        await asyncio.sleep(3)
        await update.message.reply_text(response_text)
        ###


        # 4. --- LOG THE SUCCESSFUL QUERY ---
        # We only log *after* a successful response.
        database.log_query(
            user_id=user.id,
            username=user.username,
            chat_id=chat_id
        )
        logger.info(f"Handled and logged query for user {user.id} ({user.username})")

    except Exception as e:
        logger.error(f"An error occurred while processing message for user {user.id}: {e}", exc_info=True)
        await update.message.reply_text("Sorry, an error occurred. Please try again.")
    finally:
        # 5. --- UNLOCK ---
        # This is crucial. It runs whether the `try` block succeeded or failed.
        # It ensures the user is never permanently locked.
        PROCESSING_USERS.remove(user.id)