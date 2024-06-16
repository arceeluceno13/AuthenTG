import logging
import uuid
import re

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from keep_alive import keep_alive

pattern = r'<a href="tg://user\?id=\d+">(.*?)</a>'


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
# List of allowed usernames
# List of allowed user ids
ADMIN = [1189355509,6370807036]  # Replace with actual user ids
ALLOWED_USER_IDS = []

async def token_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /token is issued."""
    user = update.effective_user
    if user.id not in ALLOWED_USER_IDS and user.id not in ADMIN:
        await update.message.reply_text("Sorry, you are not authorized to use this bot.\n"
                                        "Please contact @WizardGreyz for more information.")
        return

    s = user.mention_html()
    # Regex pattern to match the text inside the HTML tag
    pattern = r'<a href="tg://user\?id=\d+">(.*?)</a>'

    match = re.search(pattern, s)

    if match:
        # If a match is found, get the first group (the text inside the HTML tag)
        username = match.group(1)
    else:
        username = s  # If no match is found, use the original string

    # Check if a token already exists for the user
    with open("tokens.txt", "r") as f:
        for line in f:
            if line.startswith(f"{username}: {user.id}:"):
                token = line.split(": ")[2].strip()  # Get the token from the line
                break
        else:  # No token found for the user
            token = str(uuid.uuid4())  # Generate a unique token
            with open("tokens.txt", "a") as f:  # Open the file in append mode
                f.write(f"{username}: {user.id}: {token}\n")  # Write the user id and token to the file

    await update.message.reply_html(
        f"Hi {user.mention_html()}! \n"
        f"Your unique token is {token}"
    )


async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /id is issued."""
    user = update.effective_user
    await update.message.reply_text(f"Your user id is {user.id}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_message = (
        "/token - Generate a unique token.\n"
        "/id - Get your user id.\n"
        "/contact - Get the contact information.\n"
        "/help - Show this help message."
    )
    await update.message.reply_text(help_message)

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /contact is issued."""
    await update.message.reply_text("@WizardGreyz (https://t.me/WizardGreyz)")



def main() -> None:

    keep_alive()
    
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("7193483686:AAHtJurQ8TYnfTToxVfxrOLQgNq_WAr8Otc").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("token", token_command))
    application.add_handler(CommandHandler("id", id_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("contact", contact_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
