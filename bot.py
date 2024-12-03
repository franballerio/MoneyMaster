import logging
import gspread
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
# this helps to know what the bot is doing, and if there are any errors
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# this function is called when the user sends the /start command


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # object update contains information about the message
    # object context contains information about the library
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Hi Im Spendings Master, how can i help you?")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Sorry, I didn't understand that command.")


if __name__ == '__main__':
    # create the bot application (object)
    application = ApplicationBuilder().token(
        'not_my_token').build()

    # this 2 lines tell the bot what to do when /start is sent
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # this should be at the end of the file, it tells the bot what to do when an unknown command is sent
    # so this is triggered when the user sends a command that the bot doesn't know
    unknown_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    # runs the bot till ctrl+c is pressed
    application.run_polling()
