import base64
import httpx
import os
import requests 
from pyrogram import filters
from config import BOT_USERNAME
from DAXXMUSIC import app
from pyrogram import filters
import pyrogram
from uuid import uuid4
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
import aiofiles
import aiohttp
import requests

async def load_image(image_path: str, url: str) -> str:
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                async with aiofiles.open(image_path, mode="wb") as file:
                    await file.write(await response.read())
                return image_path
            return None

@app.on_message(filters.command("upscale", prefixes=["/", "!", "%", ",", "-", ".", "@", "#"]))
async def upscale_image(client, message):
    chat_id = message.chat.id
    replied_message = message.reply_to_message
    
    if not config.DEEP_API:
        return await message.reply_text("I can't upscale without a DEEP API key!")
    
    if not replied_message or not replied_message.photo:
        return await message.reply_text("Please reply to an image.")
    
    aux_message = await message.reply_text("Upscaling, please wait...")
    image_path = await replied_message.download()
    
    response = requests.post(
        "https://api.deepai.org/api/torch-srgan",
        files={'image': open(image_path, 'rb')},
        headers={'api-key': config.DEEP_API}
    ).json()
    
    image_url = response.get("output_url")
    if not image_url:
        return await aux_message.edit("Failed to upscale image, please try again.")
    
    downloaded_image = await load_image(image_path, image_url)
    if not downloaded_image:
        return await aux_message.edit("Failed to download upscaled image, please try again.")
    
    await aux_message.delete()
    await message.reply_document(document=downloaded_image)

@app.on_message(filters.command("gdraw", prefixes=["/", "!", "%", ",", "-", ".", "@", "#"]))
async def draw_image(client, message):
    chat_id = message.chat.id
    user_id = message.sender_chat.id if message.sender_chat else message.from_user.id
    replied_message = message.reply_to_message
    
    if not config.DEEP_API:
        return await message.reply_text("I can't generate images without a DEEP API key!")
    
    if replied_message and replied_message.text:
        query = replied_message.text
    elif len(message.text.split()) > 1:
        query = message.text.split(None, 1)[1]
    else:
        return await message.reply_text("Please provide text or reply to a text message.")
    
    aux_message = await message.reply_text("Generating image, please wait...")
    image_path = f"cache/{user_id}_{chat_id}_{message.id}.png"
    
    response = requests.post(
        "https://api.deepai.org/api/text2img",
        data={'text': query, 'grid_size': '1', 'image_generator_version': 'hd'},
        headers={'api-key': config.DEEP_API}
    ).json()
    
    image_url = response.get("output_url")
    if not image_url:
        return await aux_message.edit("Failed to generate image, please try again.")
    
    downloaded_image = await load_image(image_path, image_url)
    if not downloaded_image:
        return await aux_message.edit("Failed to download generated image, please try again.")
    
    await aux_message.delete()
    await message.reply_photo(photo=downloaded_image, caption=query)
# ------------


waifu_api_url = 'https://api.waifu.im/search'

# IAM_DAXX

def get_waifu_data(tags):
    params = {
        'included_tags': tags,
        'height': '>=2000'
    }

    response = requests.get(waifu_api_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None

@app.on_message(filters.command("waifu", prefixes=["/", "!", "%", ",", "-", ".", "@", "#"]))
def waifu_command(client, message):
    try:
        tags = ['maid']  # You can customize the tags as needed
        waifu_data = get_waifu_data(tags)

        if waifu_data and 'images' in waifu_data:
            first_image = waifu_data['images'][0]
            image_url = first_image['url']
            message.reply_photo(image_url)
        else:
            message.reply_text("No waifu found with the specified tags.")

    except Exception as e:
        message.reply_text(f"An error occurred: {str(e)}")
