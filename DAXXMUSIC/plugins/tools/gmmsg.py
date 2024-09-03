import random
from pyrogram import filters
from DAXXMUSIC import app

@app.on_message(filters.command(["gm", "m", "oodmorning", "ood Morning", "ood morning"], prefixes=["/", "g", "G"]))
def goodmorning_command_handler(_, message):
    sender = message.from_user.mention
    send_sticker = random.choice([True, False])
    if send_sticker:
        sticker_id = get_random_sticker()
        app.send_sticker(message.chat.id, sticker_id)
        message.reply_text(f"**Good morning, {sender}! Have a great day ahead! ☀️**")
    else:
        emoji = get_random_emoji()
        app.send_message(message.chat.id, emoji)
        message.reply_text(f"**Good morning, {sender}! Rise and shine! {emoji}**")

def get_random_sticker():
    stickers = [
        "CAACAgIAAx0CcFdGMwACAeNlwoRH7UX9bVIJpNIqBYYhpw-X6QACYgADUomRI_j-5eQN6Z1DHgQ",  # Sticker 1
        "CAACAgIAAx0CcFdGMwACAeRlwoRHt8Yjfh4Q5y4_2jEAAYCLfwAC3wEAAhZCawpKI9T0ydt5RR4E",  # Sticker 2
        "CAACAgIAAx0CcFdGMwACAeVlwoRHAAGx9qS9VpH_MNek8M1CmQACFAADwDZPE_lqX5qCa011HgQ",  # Sticker 3
        "CAACAgIAAx0CcFdGMwACAeZlwoRHJdWESGGwLXLZOsDS1QXpRgACCgADwDZPE6t8S2E4zmMNHgQ",  # Sticker 4
        "CAACAgIAAx0CcFdGMwACAedlwoRHAAFP7c0pIuK9e_D4nMDd0QACEAADwDZPE-98-xdnULKuHgQ",  # Sticker 5
    ]
    return random.choice(stickers)

def get_random_emoji():
    emojis = [
        "🌞",
        "🌅",
        "☀️",
        "🌄",
        "🌻",
    ]
    return random.choice(emojis)
