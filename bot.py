import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
# this helps to know what the bot is doing, and if there are any errors
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# function to acces sheets API


def authenticate_sheets():
    scope = ["https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "service_account.json", scope)
    try:
        gc = gspread.authorize(creds)
        return gc
    except Exception as e:
        logging.error(f"Error authenticating: {e}")
        raise


# this function is called when the user sends the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # object update contains information about the message
    # object context contains information about the library
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Hi Im Spendings Master, how can i help you?")


async def add_spending_to_sheets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        try:
            spending = context.args
            # authenticates
            gc = authenticate_sheets()
            # access the spreadsheet
            sheet = gc.open("All time spendings").sheet1

            sheet.append_row([update.effective_user.first_name,
                             update.message.date.isoformat(), spending[0], spending[1]])

            await update.message.reply_text(f"Added: {" ".join(spending)}")
        except Exception as e:
            logging.error(f"Error adding spending: {e}")
            await update.message.reply_text("Failed to add spending. Please try again.")
    else:
        await update.message.reply_text("Usage: /add <amount> <category>. Example: /add 50 groceries")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Sorry, I didn't understand that command.")


if __name__ == '__main__':
    # create the bot application (object)
    application = ApplicationBuilder().token(
        'token').build()

    # this 2 lines tell the bot what to do when /start is sent
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # this line tell the bot to add the spending
    spending_handler = CommandHandler('add', add_spending_to_sheets)
    application.add_handler(spending_handler)

    # this should be at the end of the file, it tells the bot what to do when an unknown command is sent
    # so this is triggered when the user sends a command that the bot doesn't know
    unknown_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    # runs the bot till ctrl+c is pressed
    application.run_polling()
