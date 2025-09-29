```python
# channel_post.py

import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import *
from helper_func import encode, admin


# Auto-generate links when admin sends media/files (excluding commands)
@Bot.on_message(
    filters.private
    & admin
    & ~filters.command([
        'start', 'commands', 'users', 'broadcast', 'batch', 'custom_batch',
        'genlink', 'stats', 'dlt_time', 'check_dlt_time', 'dbroadcast',
        'ban', 'unban', 'banlist', 'addchnl', 'delchnl', 'listchnl',
        'fsub_mode', 'pbroadcast', 'add_admin', 'deladmin', 'admins',
        'addpremium', 'premium_users', 'remove_premium', 'myplan', 'count'
    ])
)
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("📥 Please wait...", quote=True)
    try:
        # Copy the message into DB channel
        post_message = await message.copy(
            chat_id=client.db_channel.id,
            disable_notification=True
        )
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(
            chat_id=client.db_channel.id,
            disable_notification=True
        )
    except Exception as e:
        print(e)
        await reply_text.edit_text("⚠️ Something went wrong!")
        return

    # Encode link
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]]
    )

    # Reply to user with the sharable link
    await reply_text.edit(
        f"<b>✅ Here is your link</b>\n\n{link}",
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

    # Optional: also attach the same button to DB channel post
    if not DISABLE_CHANNEL_BUTTON:
        await post_message.edit_reply_markup(reply_markup)
```
