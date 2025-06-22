import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler 

from . import database
from . import llm_service
from . import config

logger = logging.getLogger(__name__)

# --- Concurrency Lock ---
# A set to hold the user_ids of users currently waiting for an LLM response.
PROCESSING_USERS = set()

# --- Rate Limit ---
DAILY_QUERY_LIMIT = 10

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hello {user.mention_html()}, I can process your queries for LLM. Just send your text to me. Use \model commant to choose your model.  Remember, you have {DAILY_QUERY_LIMIT} queries per day.",
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

        # Get user's current model:
        selected_model = database.get_user_model(user.id)

        # Show "typing..." status in Telegram
        await context.bot.send_chat_action(chat_id=chat_id, action='typing')
        
        # Make the expensive API call
        llm_response = await llm_service.get_llm_response(message_text, selected_model)

        await update.message.reply_text(llm_response)

        ### TEST BLOCK
        # # The placeholder response
        # response_text = (
        #     f"Echo: '{message_text}'\n\n"
        #     "(Note: LLM service is in development. This is a placeholder response.)"
        # )

        # # simulate the LLM work
        # await asyncio.sleep(3)
        # await update.message.reply_text(response_text)
        ###


        # 4. --- LOG THE SUCCESSFUL QUERY ---
        database.log_query(
            user_id=user.id,
            username=user.username,
            chat_id=update.effective_chat.id,
            model_used=selected_model
        )
        logger.info(f"Handled query for user {user.id} with model {selected_model}")

    except Exception as e:
        logger.error(f"An error occurred while processing message for user {user.id}: {e}", exc_info=True)
        await update.message.reply_text("Sorry, an error occurred. Please try again.")
    finally:
        # 5. --- UNLOCK ---
        PROCESSING_USERS.remove(user.id)


async def model_select_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with an inline keyboard for model selection."""
    keyboard = []
    # Create a button for each model in our config dictionary
    for display_name, model_id in config.models.items():
        # The 'callback_data' is what we'll get back when a user clicks the button
        button = [InlineKeyboardButton(display_name, callback_data=f"model_{model_id}")]
        keyboard.append(button)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please choose a model:", reply_markup=reply_markup)

# --- NEW: Handler for button clicks ---
async def model_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the user's model preference."""
    query = update.callback_query
    await query.answer() # Answer the callback to remove the "loading" icon on the button

    user_id = query.from_user.id
    # Extract the model ID from callback_data 
    model_id = query.data.split("model_", 1)[1]
    
    # Find the display name corresponding to the model_id
    display_name = "Unknown Model"
    for name, m_id in config.models.items():
        if m_id == model_id:
            display_name = name
            break
            
    # Update the database
    database.update_user_model(user_id, model_id)
    
    # Edit the original message to confirm the selection
    await query.edit_message_text(text=f"Model set to: {display_name}")

