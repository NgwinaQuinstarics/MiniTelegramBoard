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

if not TOKEN:
    raise ValueError(" TELEGRAM_TOKEN not found in .env file!")

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# In-memory storage (mini board)
user_posts = {}

# --- Commands ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to QuinBoard Bot!\n\n"
        "Use /help to see what I can do."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/about - About this bot\n"
        "/post <message> - Save a message\n"
        "/view - View your saved messages\n"
        "/clear - Delete all your messages\n\n"
        "You can also chat normally "
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 QuinBoard Bot\n"
        "A simple Telegram mini board bot built with Python.\n"
        "You can save and view messages easily."
    )


# --- Mini Board Features ---

async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = " ".join(context.args)

    if not message:
        await update.message.reply_text("Please provide a message.\nExample: /post Buy food")
        return

    user_posts.setdefault(user_id, []).append(message)

    await update.message.reply_text(" Message saved!")


async def view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    posts = user_posts.get(user_id, [])

    if not posts:
        await update.message.reply_text("📭 No messages saved yet.")
        return

    text = "📌 Your messages:\n\n"
    for i, msg in enumerate(posts, 1):
        text += f"{i}. {msg}\n"

    await update.message.reply_text(text)


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id in user_posts:
        user_posts[user_id] = []
        await update.message.reply_text("All messages cleared!")
    else:
        await update.message.reply_text("Nothing to clear.")


# --- Normal Chat Responses ---

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.lower()

    if "hi" in msg or "hello" in msg:
        await update.message.reply_text("Hello! Nice to meet you ")
    elif "bye" in msg:
        await update.message.reply_text("Goodbye! See you later ")
    elif "thank" in msg:
        await update.message.reply_text("You're welcome ")
    else:
        await update.message.reply_text(" I don't understand that yet. Try /help")


# --- Main ---

def main():
    print("Starting bot...")

    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("post", post))
    app.add_handler(CommandHandler("view", view))
    app.add_handler(CommandHandler("clear", clear))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print(" Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()