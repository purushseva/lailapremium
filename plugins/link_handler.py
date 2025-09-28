from pyrogram import Client, filters
import re

@Client.on_message(filters.private & filters.text)
async def handle_links(client, message):
    text = message.text.strip()

    # Match channel/group message links OR bot deep-links
    if re.match(r"^https://t\.me/(c/\d+/\d+|[A-Za-z0-9_]+/\d+|[A-Za-z0-9_]+\?start=.*)$", text):
        await message.reply("🔄 Processing your link...")

        try:
            if "?start=" in text:
                # It's a bot deep-link, just return/copy it
                await message.reply(f"✅ Bot link received!\n\n🔗 {text}")
                return

            # Else: process channel/group message links
            parts = text.replace("https://t.me/", "").split("/")
            chat_id = parts[0]
            msg_id = int(parts[1])

            # Fetch original message
            original = await client.get_messages(chat_id, msg_id)

            if not original or not original.media:
                return await message.reply("⚠️ No media found in that link!")

            # Copy media into your DB channel
            sent = await original.copy(client.db_channel.id)

            # Generate your bot’s shareable link
            new_link = f"https://t.me/{client.username}?start=msgid_{sent.id}"

            await message.reply(
                f"✅ File processed successfully!\n\n📎 New Link:\n{new_link}"
            )

        except Exception as e:
            await message.reply(f"❌ Error while processing: `{e}`")

    # ❌ Removed spamming else
    # Now the bot will just IGNORE invalid messages instead of replying
