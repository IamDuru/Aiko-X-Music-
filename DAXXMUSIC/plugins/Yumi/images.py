import requests
from requests import get 
from DAXXMUSIC import app
from pyrogram import filters
from pyrogram.types import InputMediaPhoto
import random

@app.on_message(filters.command(["image", "img"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]))
async def image_search(_, message):
    chat_id = message.chat.id

    try:
        query = message.text.split(None, 1)[1]
    except:
        return await message.reply("**ɢɪᴠᴇ ɪᴍᴀɢᴇ ɴᴀᴍᴇ ғᴏʀ sᴇᴀʀᴄʜ 🔍**")

    msg = await message.reply(f"sᴄʀᴀᴘɪɴɢ ɪᴍᴀɢᴇs ғʀᴏᴍ ᴍᴜʟᴛɪᴘʟᴇ sᴏᴜʀᴄᴇs...")

    # List of API functions
    api_functions = [
        pinterest_api,
        unsplash_api,
        lorem_picsum_api,
        shibe_online_api
    ]

    random.shuffle(api_functions)  # Randomize the order of APIs

    for api_func in api_functions:
        try:
            images = await api_func(query)
            if images:
                media_group = []
                count = 0
                for url in images[:7]:  # Changed to 7
                    media_group.append(InputMediaPhoto(media=url))
                    count += 1
                    await msg.edit(f"=> ᴏᴡᴏ sᴄʀᴀᴘᴇᴅ ɪᴍᴀɢᴇs {count}")

                await app.send_media_group(
                    chat_id=chat_id, 
                    media=media_group,
                    reply_to_message_id=message.id
                )
                await msg.delete()
                return
        except Exception as e:
            print(f"Error in {api_func.__name__}: {e}")
            continue

    await msg.edit("ɴᴏ ɪᴍᴀɢᴇs ғᴏᴜɴᴅ ᴏʀ ᴀʟʟ ᴀᴘɪs ғᴀɪʟᴇᴅ.")

async def pinterest_api(query):
    response = get(f"https://pinterest-api-one.vercel.app/?q={query}").json()
    return response.get("images", [])[:7]  # Limit to 7 images

async def unsplash_api(query):
    images = []
    for _ in range(7):  # Get 7 random images
        response = get(f"https://source.unsplash.com/random/900×700/?{query}").url
        if response and response not in images:
            images.append(response)
    return images

async def lorem_picsum_api(query):
    # Lorem Picsum doesn't support search, so we're just getting random images
    return [f"https://picsum.photos/900/700?random={i}" for i in range(7)]

async def shibe_online_api(query):
    # This API only provides dog, cat, or bird images
    animal = 'shibes'  # default to dogs
    if 'cat' in query.lower():
        animal = 'cats'
    elif 'bird' in query.lower():
        animal = 'birds'
    response = get(f"http://shibe.online/api/{animal}?count=7&urls=true").json()
    return response
