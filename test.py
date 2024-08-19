import logging
import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
SAVE_DIRECTORY = 'results'

# To store the annotation results
test_results = {}


async def test_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Save the answer
    test_results['user'] = query.from_user.username
    test_results['result'] = query.data

    if query.data == 'error':


        keyboard = [
            [InlineKeyboardButton("Reason 1", callback_data='1')],
            [InlineKeyboardButton("Reason 2", callback_data='2')],
            [InlineKeyboardButton("Reason 3", callback_data='3')],
            [InlineKeyboardButton("Reason 4", callback_data='4')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_caption('')
        await query.edit_message_reply_markup(reply_markup=reply_markup)

        return

    keyboard = [
        [InlineKeyboardButton("HIV", callback_data='1')],
        [InlineKeyboardButton("Hepatitis", callback_data='2')],
        [InlineKeyboardButton("Syphilis", callback_data='3')],
        [InlineKeyboardButton("Chlamydia", callback_data='4')],
        [InlineKeyboardButton("Gonorrhea", callback_data='5')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_caption('')
    await query.edit_message_reply_markup(reply_markup=reply_markup)


async def save_results(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Save the answer
    test_results['type'] = query.data
    username = query.from_user.username
    message_id = query.message.message_id

    # Save the results
    file_path = os.path.join(SAVE_DIRECTORY, f"{username}_{message_id}.json")
    with open(file_path, 'w') as json_file:
        json.dump(test_results, json_file, indent=4)

    await query.edit_message_reply_markup(reply_markup=None)
    await query.edit_message_caption(f"✅ Saved. Results: {test_results['result']}, {test_results['type']}")


if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CallbackQueryHandler(test_type, pattern='^(positive|negative|error)$'))
    app.add_handler(CallbackQueryHandler(save_results, pattern='^[1-5]$'))

    app.run_polling()
