import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables from .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Safety check
if not TOKEN:
    raise ValueError("No TELEGRAM_TOKEN found in .env! Make sure the file exists and the variable is correct.")

# --- Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to your mini board bot!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.lower()
    
    if "hi" in msg or "hello" in msg:
        await update.message.reply_text("Hello! Nice to meet you.")
    elif "bye" in msg or "goodbye" in msg:
        await update.message.reply_text("Goodbye! See you later.")
    else:
        await update.message.reply_text("I don't understand that yet.")

# --- Main Bot Setup ---

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))

    # Message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()