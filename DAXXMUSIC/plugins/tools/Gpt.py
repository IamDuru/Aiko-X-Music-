import openai
import time
import requests
import logging
from DAXXMUSIC import app
from config import BOT_USERNAME, GPT_API

from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Set up OpenAI API
openai.api_key = GPT_API
MODEL = "text-davinci-003"  # Specify your model here

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class APIError(Exception):
    """Custom exception for API errors"""
    pass

class ResponseParsingError(Exception):
    """Custom exception for response parsing errors"""
    pass

@app.on_message(filters.command(["chatgpt", "ai", "ask", "gpt", "solve"], prefixes=["+", ".", "/", "-", "", "$", "#", "&"]))
async def chat_gpt(bot, message):
    try:
        start_time = time.time()
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

        # Check if the command has the required arguments
        if len(message.command) < 2:
            await message.reply_text(
                "Example:\n\n/chatgpt Ram Ram Bhai Sariyane...!!",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Ask again", switch_inline_query_current_chat="")]]
                )
            )
            return

        # Extract the query from the message
        query = message.text.split(' ', 1)[1]
        logging.info(f'Received query: {query}')
        
        # API request to the OpenAI service
        response = openai.Completion.create(
            engine=MODEL,
            prompt=query,
            max_tokens=150
        )
        
        try:
            answer = response.choices[0].text.strip()
            end_time = time.time()
            telegram_ping = str(round((end_time - start_time) * 1000, 3)) + " ms"
            
            # Send the bot response with enhanced UI
            await message.reply_text(
                f"**Query:** {query}\n\n"
                f"**Answer:** {answer}\n\n"
                f"_Answered by @{BOT_USERNAME}\n"
                f"`Response time: {telegram_ping}`",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("ᴀsᴋ ᴀɴᴏᴛʜᴇʀ ǫᴜᴇsᴛɪᴏɴ", switch_inline_query_current_chat="")],
                        [InlineKeyboardButton("⊛ ʜᴇʟᴘ ⊛", url="https://t.me/{BOT_USERNAME}?start=help")],
                        [InlineKeyboardButton("⊛ sᴜᴘᴘᴏʀᴛ ⊛", url="https://t.me/DNS_NETWORK")]
                    ]
                )
            )
            logging.info(f'Successfully answered query: {query} in {telegram_ping}')
        except KeyError as e:
            # Handle KeyError specifically
            logging.error(f'KeyError while parsing response: {e}')
            await message.reply_text("Error accessing the response.")
        except Exception as e:
            # Handle any other exception that might occur
            logging.error(f'Error: {e}')
            await message.reply_text(f"**Error: {e}**")
    except Exception as e:
        logging.error(f'Unexpected error: {e}')
        await message.reply_text(f"**Error: {e}**")

# Command for GPT chat with user's name
@app.on_message(filters.command(["ra"], prefixes=["e", "E"]))
async def chat_arvis(app, message):
    try:
        await app.send_chat_action(message.chat.id, ChatAction.TYPING)
        name = message.from_user.first_name
        if len(message.command) < 2:
            await message.reply_text(f"**Hello {name}, I am Era. How can I help you today?**")
        else:
            query = message.text.split(' ', 1)[1]
            resp = openai.ChatCompletion.create(
                model=MODEL,
                messages=[{"role": "user", "content": query}],
                temperature=0.2
            )
            response_text = resp['choices'][0]["message"]["content"]
            await message.reply_text(response_text)
    except Exception as e:
        await message.reply_text(f"**Error:** {e}")

# Future Improvements:
# 1. Implement caching to reduce redundant API requests for the same query.
# 2. Use a more reliable error handling mechanism for different types of API responses.
# 3. Add rate limiting to handle API throttling.
# 4. Expand user instructions and add more detailed usage guidelines.
# 5. Enhance performance by parallelizing requests if handling multiple queries simultaneously.
