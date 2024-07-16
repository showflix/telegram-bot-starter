import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Telegram bot token
TELEGRAM_BOT_TOKEN = '5667861898:AAGx1IPp4FjbvWOvzDjzXW8ukoQ3YxlS6qY'

# Cloudflare Worker URL
CLOUDFLARE_WORKER_URL = 'https://fileserver.videoshowflix.workers.dev/'

# Initialize the Telegram bot
updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Command handler for starting the bot
def start(update, context):
    update.message.reply_text('Hello! Send me a file and I will provide a streamable link.')

# Handler for file messages
def handle_file(update, context):
    file_id = update.message.document.file_id
    file_name = update.message.document.file_name
    file_size = update.message.document.file_size
    
    try:
        # Fetch file details from Telegram
        file_info = context.bot.get_file(file_id)
        file_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_info.file_path}"

        # Prepare request to Cloudflare Worker for streaming link
        cloudflare_worker_url = f"{CLOUDFLARE_WORKER_URL}stream/{file_id}"
        response = requests.get(cloudflare_worker_url)

        if response.ok:
            streamable_link = response.text.strip()
            update.message.reply_text(f"Streamable link for '{file_name}' ({file_size} bytes):\n{streamable_link}")
        else:
            update.message.reply_text("Error: Failed to generate streamable link.")

    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

# Error handler
def error(update, context):
    update.message.reply_text(f"An error occurred: {context.error}")

# Add handlers to the dispatcher
start_handler = CommandHandler('start', start)
file_handler = MessageHandler(Filters.document, handle_file)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(file_handler)
dispatcher.add_error_handler(error)

# Start the bot
updater.start_polling()
updater.idle()
