import os
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GITHUB_TOKEN = os.getenv("GH_TOKEN")

# Your repo details
OWNER = "tansique-17"
REPO = "tryhackme-streak-bot"
WORKFLOW_FILE = "thm.yml"
REF = "main"  # branch to run on

# -------------------------------
# Trigger GitHub Workflow
# -------------------------------
def trigger_github_workflow() -> bool:
    """Send a dispatch event to GitHub Actions workflow."""
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW_FILE}/dispatches"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    }
    data = {"ref": REF}
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 204:
        logger.info("✅ Workflow triggered successfully.")
        return True
    else:
        logger.error(f"❌ Failed to trigger workflow: {response.status_code}, {response.text}")
        return False


# -------------------------------
# Telegram Bot Handlers
# -------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send start message with button."""
    keyboard = [
        [InlineKeyboardButton("🚀 Trigger TryHackMe Workflow", callback_data='trigger_workflow')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Hey Tansique! Want to trigger the streak bot?", reply_markup=reply_markup)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button press."""
    query = update.callback_query
    await query.answer()

    if query.data == "trigger_workflow":
        await query.edit_message_text("⏳ Triggering GitHub workflow... please wait.")
        success = trigger_github_workflow()
        if success:
            await context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="✅ Workflow successfully triggered on GitHub!")
        else:
            await context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="❌ Failed to trigger workflow. Check logs or token.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Simple help command."""
    await update.message.reply_text("Use /start to get the trigger button.")


# -------------------------------
# Main Entry
# -------------------------------
def main():
    """Start the Telegram bot."""
    if not all([TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, GITHUB_TOKEN]):
        raise ValueError("Missing required environment variables!")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_callback))

    logger.info("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
