import os
import time
import signal
from loguru import logger

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler


# Enable logging
'''
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
'''

#logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )
    
def start_with_keyboard(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data='1'),
            InlineKeyboardButton("Option 2", callback_data='2'),
        ],
        [InlineKeyboardButton("Option 3", callback_data='3')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)   

def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    query.edit_message_text(text=f"Selected option: {query.data}")


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    logger.debug(update)
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    logger.debug(update)
    update.message.reply_text(update.message.text)
    
def kill_bot() -> None:
    os.kill(os.getpid(), signal.SIGINT)       
#    os.kill(os.getpid(), signal.SIGKILL)
    

def main() -> None:
    try:
        """Start the bot."""
        logger.info("Bot initializing")
        
        # Create the Updater and pass it your bot's token.
        # updater = Updater("TOKEN")
        
        # or use system variable
        updater = Updater(os.getenv('API_KEY'))
        
        # Get the dispatcher to register handlers
        dispatcher = updater.dispatcher

        # on different commands - answer in Telegram
        dispatcher.add_handler(CommandHandler("start", start_with_keyboard))
        dispatcher.add_handler(CommandHandler("help", help_command))
        updater.dispatcher.add_handler(CallbackQueryHandler(button))

        # on non command i.e message - echo the message on Telegram
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

        # Start the Bot
        updater.start_polling()
        
        logger.info("Bot is ready")

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        # updater.idle()

        while True:
            time.sleep(1)
    except (KeyboardInterrupt, Exception) as err:
        pass
        
    logger.info("Kill the bot on main")
    kill_bot()
    
        
if __name__ == '__main__':
    main()
    
