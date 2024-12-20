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
            spending = update.message.text.split(" ", 1)
            spending = [i.strip() for i in spending[1].split(',')]
            # authenticates
            gc = authenticate_sheets()
            # access the spreadsheet
            sheet = gc.open("All time spendings").sheet1

            date = update.message.date.isoformat(
                sep=" ").split(" ")[0].split("-")

            sheet.append_row([update.effective_user.first_name, date[0], date[1], date[2],
                              spending[0], spending[1], spending[2]], "USER_ENTERED")

            await update.message.reply_text(f"Added: {spending[1]} ✅✅")
        except Exception as e:
            logging.error(f"Error adding spending: {e}")
            await update.message.reply_text("Failed to add spending. Please try again.")
    else:
        await update.message.reply_text("Usage: /add <amount>, <product>, <category>. Example: /add 50,candy,groceries, ")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Sorry, I didn't understand that command.")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Sorry, I didn't understand that command.")


async def spent_month_func(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        today = update.message.date.isoformat(
            sep=" ").split(" ")[0].split("-")

        month = context.args[0] if context.args else today[1]

        gc = authenticate_sheets()
        sheet = gc.open("All time spendings").worksheet("Months")
        data = sheet.get_all_records()  # this returns a dict of lists

        # await update.message.reply_text(f"{data}")

        spent = 0

        for row in data:
            if (row["Year"] == int(today[0]) and row["Month"] == int(month)):
                spent += int(row["Amount"])

        months = {
            "1": "January",
            "2": "February",
            "3": "March",
            "4": "April",
            "5": "May",
            "6": "June",
            "7": "July",
            "8": "August",
            "9": "September",
            "10": "October",
            "11": "November",
            "12": "December"
        }

        await update.message.reply_text(f"You spent ${spent} in {months[month]}")

    except Exception as e:
        logging.error(f"Error getting spent: {e}")
        await update.message.reply_text("Failed to get spent. Please try again.")


async def spent_day_func(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (context.args):
        try:
            date = context.args[0].split("/")
            day, month, year = date
            gc = authenticate_sheets()
            sheet = gc.open("All time spendings").worksheet("Days")
            data = sheet.get_all_records()  # this returns a dict of lists

            spent = 0

            for row in data:
                if (row["Year"] == int(year) and row["Month"] == int(month) and row["Day"] == int(day)):
                    spent += int(row["Amount"])

            await update.message.reply_text(f"On {day}/{month}/{year}, you spent ${spent}")

        except Exception as e:
            logging.error(f"Error getting spent: {e}")
            await update.message.reply_text("Failed to get spent. Please try again.")

    else:
        await update.message.reply_text("Please enter a valid date format, dd/mm/yyyy")


async def delete_spending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gc = authenticate_sheets()
    sheet = gc.open("All time spendings").sheet1
    sheet.delete_rows(len(sheet.get_all_records()) + 1)

    await update.message.reply_text("Last expense deleted")


if __name__ == '__main__':
    # create the bot application (object)
    application = ApplicationBuilder().token(
        'Token').build()

    # this 2 lines tell the bot what to do when /start is sent
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # spendings_handler = CommandHandler('adds', add_spending)
    # application.add_handler(spendings_handler)

    spending_handler = CommandHandler('add', add_spending_to_sheets)
    application.add_handler(spending_handler)

    spent_month = CommandHandler("balance", spent_month_func)
    application.add_handler(spent_month)

    spent_day = CommandHandler("spent", spent_day_func)
    application.add_handler(spent_day)

    delete_handler = CommandHandler("undo", delete_spending)
    application.add_handler(delete_handler)

    # this should be at the end of the file, it tells the bot what to do when an unknown command is sent
    # so this is triggered when the user sends a command that the bot doesn't know
    unknown_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    # runs the bot till ctrl+c is pressed
    application.run_polling()
