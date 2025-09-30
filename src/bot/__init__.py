"""
Telegram bot for getting user and chat IDs from messages.
"""

import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Bot token from environment
BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Handle /start command - show user ID and current chat ID.
    """
    user = update.effective_user
    chat = update.effective_chat

    if not update.message:
        return

    if not user or not chat:
        await update.message.reply_text(
            "Unable to get user or chat information.",
        )
        return

    response = f"Your user ID: {user.id}\n"
    response += f"Current chat ID: {chat.id}"

    await update.message.reply_text(response)


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Handle /help command - show detailed help information.
    """
    help_text = (
        "I will send you your telegram user ID, "
        "current chat ID and sender ID or "
        "chat ID of forwarded message.\n\n"
        "User ID - your unique identifier in telegram, "
        "which you can use in your "
        "telegram bot. Read more: https://core.telegram.org/bots/api#user\n\n"
        "Commands:\n"
        "/start - Get your user ID and current chat ID\n"
        "/help - Show this help message\n\n"
        "You can also forward any message to me to get the sender's ID and "
        "original chat ID."
    )
    if not update.message:
        return

    await update.message.reply_text(help_text)


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Handle regular messages and forwarded messages to extract IDs.
    """
    message = update.message

    if not message:
        return

    # Get basic IDs
    user_id = update.effective_user.id if update.effective_user else "Unknown"
    chat_id = update.effective_chat.id if update.effective_chat else "Unknown"

    response_parts = [
        f"Your user ID: {user_id}",
        f"Current chat ID: {chat_id}",
    ]

    # Check if message is forwarded
    if message.forward_from:
        # Message forwarded from a user
        response_parts.append(
            f"Forwarded from user ID: {message.forward_from.id}",
        )
        if message.forward_from.username:
            response_parts.append(
                f"Forwarded from username: @{message.forward_from.username}",
            )

    elif message.forward_from_chat:
        # Message forwarded from a channel/group
        response_parts.append(
            f"Forwarded from chat ID: {message.forward_from_chat.id}",
        )
        response_parts.append(
            f"Forwarded from chat title: {message.forward_from_chat.title}",
        )
        if message.forward_from_chat.username:
            response_parts.append(
                "Forwarded from chat "
                f"username: @{message.forward_from_chat.username}",
            )

    elif message.forward_sender_name:
        # Message forwarded from a user who has privacy settings enabled
        response_parts.append(
            f"Forwarded from sender name: {message.forward_sender_name}",
        )

    # Check for reply to message
    if message.reply_to_message:
        reply_user = message.reply_to_message.from_user
        if reply_user:
            response_parts.append(f"Replying to user ID: {reply_user.id}")
            if reply_user.username:
                response_parts.append(
                    f"Replying to username: @{reply_user.username}",
                )

    # Check for message sender (if different from effective user)
    if message.from_user and message.from_user.id != user_id:
        response_parts.append(f"Message sender ID: {message.from_user.id}")
        if message.from_user.username:
            response_parts.append(
                f"Message sender username: @{message.from_user.username}",
            )

    response = "\n".join(response_parts)
    await message.reply_text(response)


def main() -> None:
    """
    Main function to start the bot.
    """
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN environment variable is required")

    # Create application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    # Add message handler for all other messages
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message),
    )

    # Start the bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
