import logging
from telegram import Update, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, Updater, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler, ConversationHandler
from telegram.constants import ParseMode

token = "7735203801:AAGwegnbEhqjLWGI-3QgmLz3iM53TvPShaU"

async def start(update: Update, context: CallbackContext) -> None:
    """Handle the /start command and show inline buttons."""
    keyboard = [
        [InlineKeyboardButton("Add Spending", callback_data='add')],
        [InlineKeyboardButton("View Spendings", callback_data='view')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            "Hello, I'm the spendings bot. I can help you keep track of your spendings. "
            "Choose an option below:",
            reply_markup=reply_markup
        )

# async def help():


async def buttons(update: Update, context: CallbackContext) -> None:
    """Send a message with buttons."""
    keyboard = [
        [InlineKeyboardButton("Option 1", callback_data='1')],
        [InlineKeyboardButton("Option 2", callback_data='2')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text("Choose an option:", reply_markup=reply_markup)

async def buttons_callback(update: Update, context: CallbackContext) -> None:
    """Handle button clicks."""
    query = update.callback_query
    if query:  # Ensure there's a valid callback query
        await query.answer()  # Acknowledge the callback query (prevents loading spinner)

        # Get the callback data and perform an action
        callback_data = query.data

        if callback_data == 'add':
            await query.edit_message_text(text="You selected to add a spending!")
        elif callback_data == 'view':
            await query.edit_message_text(text="You selected to view your spendings.")
        else:
            await query.edit_message_text(text="Unknown option selected.")


def main():
    "This function starts the bot."
    # creates the bot application
    app = Application.builder().token(token).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    # app.add_handler(CommandHandler("", ))
    #
    # Register callback handler for buttons
    app.add_handler(CallbackQueryHandler(buttons_callback))

    app.run_polling() # this runs the bot

if __name__ == "__main__":
    main()
