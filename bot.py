from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Dictionary to store subscriber info
subscribers = {}

# --- Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message for /start command"""
    user = update.effective_user
    await update.message.reply_text(
        f"Welcome to your mini board bot, {user.first_name}!\n"
        "Type /help to see available commands."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List available commands"""
    commands = (
        "/start - Start the bot\n"
        "/help - Show commands\n"
        "/subscribe - Add your name, email, phone\n"
        "/board - See all subscribers"
    )
    await update.message.reply_text(f"Available commands:\n{commands}")

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Initiate subscription flow"""
    user_id = update.effective_user.id
    subscribers[user_id] = {"name": None, "email": None, "phone": None}
    await update.message.reply_text("Let's subscribe you! What's your name?")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle general messages and subscription flow"""
    user_id = update.effective_user.id
    text = update.message.text.lower()

    # Subscription flow
    if user_id in subscribers:
        user_data = subscribers[user_id]
        if user_data["name"] is None:
            user_data["name"] = update.message.text
            await update.message.reply_text("Great! Now enter your email:")
        elif user_data["email"] is None:
            user_data["email"] = update.message.text
            await update.message.reply_text("Awesome! Finally, enter your phone number:")
        elif user_data["phone"] is None:
            user_data["phone"] = update.message.text
            await update.message.reply_text(
                f"Thanks for subscribing, {user_data['name']}!\n"
                "You are now added to the board."
            )
        return

    # Basic chat responses
    if "hi" in text:
        await update.message.reply_text("Hello! Nice to meet you.")
    elif "how are you" in text:
        await update.message.reply_text("I'm doing great, thanks for asking!")
    elif "bye" in text:
        await update.message.reply_text("Goodbye! See you soon.")
    else:
        await update.message.reply_text("I don't understand that yet. Try /help!")

async def board(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show all subscribed users"""
    if not subscribers:
        await update.message.reply_text("No subscribers yet.")
        return
    msg = "Subscribers:\n"
    for user in subscribers.values():
        if user["name"]:
            msg += f"- {user['name']} ({user['email']}, {user['phone']})\n"
    await update.message.reply_text(msg)

# --- Bot Setup ---
if __name__ == "__main__":
    # Bot token from BotFather
    TOKEN = "8636846068:AAGcUZEXSRLhNVtlOQcqjKwH1VyHrGCHGQ4"

    app = ApplicationBuilder().token(TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CommandHandler("board", board))

    # Message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("Bot is running...")
    app.run_polling()