import os
import logging
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

# Validate token
if not TOKEN:
    raise ValueError(" TELEGRAM_TOKEN not found in .env file!")

# Enable logging 
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

# --- Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to QuinBoard Bot!\n\n"
        "Send me a message and I'll respond.\n"
        "Try: hi, hello, bye"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()

    if "hi" in user_message or "hello" in user_message:
        await update.message.reply_text("Hello! Nice to meet you.")
    elif "bye" in user_message:
        await update.message.reply_text("Goodbye! See you later.")
    elif "thank" in user_message:
        await update.message.reply_text("You're welcome ")
    else:
        await update.message.reply_text("I don't understand that yet ")


# --- Main Function ---

def main():
    print(" Starting bot...")

    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print(" Bot is running...")

    # Start polling
    app.run_polling()


if __name__ == "__main__":
    main()