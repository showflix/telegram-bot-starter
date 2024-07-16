from pyrogram import Client, filters
import requests

# Telegram bot token
API_ID = "14959925"
API_HASH = "a8d3503be0455c779a17193e48cab451"
BOT_TOKEN = "5667861898:AAGx1IPp4FjbvWOvzDjzXW8ukoQ3YxlS6qY"

# Cloudflare Worker URL
CLOUDFLARE_WORKER_URL = "https://fileserver.videoshowflix.workers.dev/"

# Initialize Pyrogram Client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@app.on_message(filters.document)
async def handle_file(client, message):
    try:
        # Extract file details
        file_id = message.document.file_id
        file_name = message.document.file_name
        file_size = message.document.file_size

        # Generate streamable link using Cloudflare Worker
        cloudflare_worker_url = f"{CLOUDFLARE_WORKER_URL}stream/{file_id}"
        response = requests.get(cloudflare_worker_url)

        if response.ok:
            streamable_link = response.text.strip()
            await message.reply_text(f"Streamable link for '{file_name}' ({file_size} bytes):\n{streamable_link}")
        else:
            await message.reply_text("Error: Failed to generate streamable link.")

    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")


# Start the bot
app.run()
