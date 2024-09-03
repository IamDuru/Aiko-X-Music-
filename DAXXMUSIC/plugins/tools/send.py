from DAXXMUSIC import app
from pyrogram import filters
from pyrogram.types import Message

@app.on_message(filters.command("send", prefixes=["/", "!", "%", ",", "-", ".", "@", "#"]))
async def send_html(client, message: Message):
    # Check if the user is an admin
    try:
        user = await message.chat.get_member(message.from_user.id)
        if user.status not in ["creator", "administrator"]:
            await message.reply_text("You don't have permission to use this command.")
            return
    except Exception as e:
        print(f"Error checking user status: {e}")
        await message.reply_text("An error occurred while checking permissions.")
        return

    # Get the message content after the command and prefix
    if len(message.text.split(None, 1)) < 2:
        await message.reply_text("Please provide a message to send.")
        return

    html_message = message.text.split(None, 1)[1]

    try:
        # Send the message with HTML parsing
        await message.reply_text(
            text=html_message,
            parse_mode="html"
        )
    except Exception as e:
        await message.reply_text(f"Error sending message: {str(e)}")

# Note: You don't need to call app.run() here, as it's likely handled in your main script
