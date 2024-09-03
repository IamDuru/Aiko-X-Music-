import asyncio, os, time, aiohttp
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from asyncio import sleep
from DAXXMUSIC import app
from pyrogram import filters, Client, enums
from pyrogram.enums import ParseMode
from pyrogram.types import *
from typing import Union, Optional
import random

random_photo = [
    "https://telegra.ph/file/1949480f01355b4e87d26.jpg",
    "https://telegra.ph/file/3ef2cc0ad2bc548bafb30.jpg",
    "https://telegra.ph/file/a7d663cd2de689b811729.jpg",
    "https://telegra.ph/file/6f19dc23847f5b005e922.jpg",
    "https://telegra.ph/file/2973150dd62fd27a3a6ba.jpg",
]

# --------------------------------------------------------------------------------- #


get_font = lambda font_size, font_path: ImageFont.truetype(font_path, font_size)
resize_text = (
    lambda text_size, text: (text[:text_size] + "...").upper()
    if len(text) > text_size
    else text.upper()
)

# --------------------------------------------------------------------------------- #


async def get_userinfo_img(
    bg_path: str,
    font_path: str,
    user_id: Union[int, str],    
    profile_path: Optional[str] = None
):
    bg = Image.open(bg_path)

    if profile_path:
        img = Image.open(profile_path)
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.pieslice([(0, 0), img.size], 0, 360, fill=255)

        circular_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        circular_img.paste(img, (0, 0), mask)
        resized = circular_img.resize((400, 400))
        bg.paste(resized, (440, 160), resized)

    img_draw = ImageDraw.Draw(bg)

    img_draw.text(
        (529, 627),
        text=str(user_id).upper(),
        font=get_font(46, font_path),
        fill=(255, 255, 255),
    )


    path = f"./userinfo_img_{user_id}.png"
    bg.save(path)
    return path
   

# --------------------------------------------------------------------------------- #

bg_path = "DAXXMUSIC/assets/userinfo.png"
font_path = "DAXXMUSIC/assets/hiroko.ttf"

# --------------------------------------------------------------------------------- #


INFO_TEXT = """**
╔════════「👤 𝐔𝐒𝐄𝐑 𝐈𝐍𝐅𝐎 👤」════════╗

👤 𝐁𝐀𝐒𝐈𝐂 𝐈𝐍𝐅𝐎𝐑𝐌𝐀𝐓𝐈𝐎𝐍
• 𝐈𝐃: `{}`
• 𝐅𝐈𝐑𝐒𝐓 𝐍𝐀𝐌𝐄: {}
• 𝐋𝐀𝐒𝐓 𝐍𝐀𝐌𝐄: {}
• 𝐔𝐒𝐄𝐑𝐍𝐀𝐌𝐄: @{}
• 𝐌𝐄𝐍𝐓𝐈𝐎𝐍: {}

📊 𝐒𝐓𝐀𝐓𝐔𝐒 𝐈𝐍𝐅𝐎𝐑𝐌𝐀𝐓𝐈𝐎𝐍
• 𝐋𝐀𝐒𝐓 𝐒𝐄𝐄𝐍: {}
• 𝐃𝐂 𝐈𝐃: {}

📝 𝐏𝐑𝐎𝐅𝐈𝐋𝐄 𝐃𝐄𝐓𝐀𝐈𝐋𝐒
• 𝐁𝐈𝐎: `{}`

• 𝐏𝐑𝐎𝐅𝐈𝐋𝐄 𝐏𝐈𝐂𝐒: {}
• 𝐀𝐍𝐈𝐌𝐀𝐓𝐄𝐃 𝐏𝐅𝐏: {}
• 𝐔𝐒𝐄𝐑 𝐓𝐘𝐏𝐄: {}

🛡️ 𝐀𝐂𝐂𝐎𝐔𝐍𝐓 𝐒𝐓𝐀𝐓𝐔𝐒
• 𝐕𝐄𝐑𝐈𝐅𝐈𝐄𝐃: {}
• 𝐑𝐄𝐒𝐓𝐑𝐈𝐂𝐓𝐄𝐃: {}
• 𝐒𝐂𝐀𝐌: {}
• 𝐅𝐀𝐊𝐄: {}
• 𝐏𝐑𝐄𝐌𝐈𝐔𝐌: {}

ℹ️ 𝐀𝐃𝐃𝐈𝐓𝐈𝐎𝐍𝐀𝐋 𝐈𝐍𝐅𝐎
• 𝐀𝐂𝐂𝐎𝐔𝐍𝐓 𝐂𝐑𝐄𝐀𝐓𝐄𝐃: {}
• 𝐂𝐎𝐌𝐌𝐎𝐍 𝐂𝐇𝐀𝐓𝐒: {}
• 𝐔𝐒𝐄𝐑 𝐋𝐀𝐍𝐆: {}

╚════════「🌟 𝐄𝐍𝐃 𝐎𝐅 𝐈𝐍𝐅𝐎 🌟」════════╝**
"""

# --------------------------------------------------------------------------------- #

async def userstatus(user_id):
   try:
      user = await app.get_users(user_id)
      x = user.status
      if x == enums.UserStatus.RECENTLY:
         return "Recently"
      elif x == enums.UserStatus.LAST_WEEK:
          return "Last week"
      elif x == enums.UserStatus.LONG_AGO:
          return "Long time ago"
      elif x == enums.UserStatus.OFFLINE:
          return "Offline"
      elif x == enums.UserStatus.ONLINE:
         return "Online"
   except:
        return "**𝐒𝐎𝐌𝐄𝐓𝐇𝐈𝐍𝐆 𝐖𝐄𝐍𝐓 𝐖𝐑𝐎𝐍𝐆!**"
    

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(["info", "userinfo"], prefixes=["/", "!", "%", ",", "-", ".", "@", "#"]))
async def userinfo(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    async def get_user_info(user_id):
        try:
            user_info = await app.get_chat(user_id)
            user = await app.get_users(user_id)
            status = await userstatus(user.id)
            id = user_info.id
            dc_id = user.dc_id or "Unknown"
            first_name = user_info.first_name 
            last_name = user_info.last_name if user_info.last_name else "No last name"
            username = user_info.username if user_info.username else "No Username"
            mention = user.mention
            bio = user_info.bio if user_info.bio else "No bio set"
            profile_pics = await app.get_chat_photos_count(user_id)
            is_animated = "Yes" if user.photo and user.photo.is_animated else "No"
            user_type = "Bot" if user.is_bot else "Human"
            is_verified = "Yes" if user.is_verified else "No"
            is_restricted = "Yes" if user.is_restricted else "No"
            is_scam = "Yes" if user.is_scam else "No"
            is_fake = "Yes" if user.is_fake else "No"
            is_premium = "Yes" if user.is_premium else "No"
            joined_date = user.joined_date.strftime("%Y-%m-%d %H:%M:%S") if user.joined_date else "Unknown"
            common_chats = len(await user.get_common_chats())
            language_code = user.language_code or "Unknown"

            return (id, first_name, last_name, username, mention, status, dc_id, bio, 
                    profile_pics, is_animated, user_type, is_verified, is_restricted, 
                    is_scam, is_fake, is_premium, joined_date, common_chats, language_code)
        except Exception as e:
            return str(e)

    if not message.reply_to_message and len(message.command) == 2:
        try:
            user_id = message.text.split(None, 1)[1]
            user_info = await get_user_info(user_id)
            if isinstance(user_info, tuple):
                await message.reply_text(INFO_TEXT.format(*user_info))
            else:
                await message.reply_text(user_info)
        except Exception as e:
            await message.reply_text(str(e))        
    
    elif not message.reply_to_message:
        try:
            user_info = await get_user_info(user_id)
            if isinstance(user_info, tuple):
                await message.reply_text(INFO_TEXT.format(*user_info))
            else:
                await message.reply_text(user_info)
        except Exception as e:
            await message.reply_text(str(e))

    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        try:
            user_info = await get_user_info(user_id)
            if isinstance(user_info, tuple):
                await message.reply_text(INFO_TEXT.format(*user_info))
            else:
                await message.reply_text(user_info)
        except Exception as e:
            await message.reply_text(str(e))
                
