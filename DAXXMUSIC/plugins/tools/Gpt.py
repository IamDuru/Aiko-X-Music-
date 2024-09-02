import time
import requests
import logging
from DAXXMUSIC import app
from config import BOT_USERNAME

from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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
                    [[InlineKeyboardButton("ᴀsᴋ ᴀɢᴀɪɴ", switch_inline_query_current_chat="")]]
                )
            )
            return

        # Extract the query from the message
        query = message.text.split(' ', 1)[1]
        logging.info(f'Received query: {query}')
        
        # API request to the ChatGPT service
        response = requests.get(f'https://chatgpt.apinepdev.workers.dev/?question={query}')
        
        # Raise an error if the API call was unsuccessful
        if response.status_code != 200:
            raise APIError(f'API request failed with status code {response.status_code}')
        
        try:
            # Parse the JSON response
            json_response = response.json()
            if "answer" in json_response:
                answer = json_response["answer"]
                end_time = time.time()
                telegram_ping = str(round((end_time - start_time) * 1000, 3)) + " ms"
                
                # Send the bot response with enhanced UI
                await message.reply_text(
                    f"**Query:** {query}\n\n"
                    f"**Answer:** {answer}\n\n"
                    f"_Answered by @{BOT_USERNAME}_\n"
                    f"`Response time: {telegram_ping}`",
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton("ᴀsᴋ ᴀɴᴏᴛʜᴇʀ ǫᴜᴇsᴛɪᴏɴ", switch_inline_query_current_chat="")],
                            [InlineKeyboardButton("⊛ ʜᴇʟᴘ ⊛", url="https://t.me/EraVibesXbot?start=help")],
                            [InlineKeyboardButton("⊛ ʙɪɢ ᴜᴘᴅᴀᴛᴇs ⊛", url="https://t.me/DNS_NETWORK")]
                        ]
                    )
                )
                logging.info(f'Successfully answered query: {query} in {telegram_ping}')
            else:
                raise ResponseParsingError("No 'answer' key found in the response.")
        except KeyError as e:
            # Handle KeyError specifically
            logging.error(f'KeyError while parsing response: {e}')
            await message.reply_text("Error accessing the response.")
        except ResponseParsingError as e:
            # Handle custom response parsing errors
            logging.error(f'ResponseParsingError: {e}')
            await message.reply_text(str(e))
    except APIError as e:
        logging.error(f'APIError: {e}')
        await message.reply_text(f"API Error: {e}")
    except Exception as e:
        # Catch-all for any other exceptions
        logging.error(f'Unexpected error: {e}')
        await message.reply_text(f"**Error: {e}**")

# Future Improvements:
# 1. Implement caching to reduce redundant API requests for the same query.
# 2. Use a more reliable error handling mechanism for different types of API responses.
# 3. Add rate limiting to handle API throttling.
# 4. Expand user instructions and add more detailed usage guidelines.
# 5. Enhance performance by parallelizing requests if handling multiple queries simultaneously.
