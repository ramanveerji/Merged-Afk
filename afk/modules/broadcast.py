import asyncio
from pyrogramv1 import filters
from pyrogramv1.errors import FloodWait
from pyrogramv1.types import Message
from afk import SUDOERS, app
from afk.database import get_afk_users, get_served_chats

@app.on_message(filters.command("afkusers") & filters.user(SUDOERS))
async def total_users(_, message: Message):
    afk_users = []
    try:
        chats = await get_afk_users()
        for chat in chats:
            afk_users.append(int(chat["user_id"]))
    except Exception as e:
        return await message.reply_text(f"**Error:-** {e}")
    users = len(afk_users)
    return await message.reply_text(
        f"Total AFK Users on Bot:- **{users}**"
    )

@app.on_message(filters.command("broadcast") & filters.user(SUDOERS))
async def broadcast(_, message):
    if message.reply_to_message:
        x = message.reply_to_message.text
        y = message.chat.id
    else:
        if len(message.command) < 2:
            return await message.reply_text(
                "**Usage**:\n/broadcast [MESSAGE] or [Reply to a Message]"
            )
        query = message.text.split(None, 1)[1]
    sent = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            await app.send_message(
                i, text=x if message.reply_to_message else query
            )
            sent += 1
        except FloodWait as e:
            flood_time = int(e.x)
            if flood_time > 200:
                continue
            await asyncio.sleep(flood_time)
        except Exception:
            continue
    try:
        await message.reply_text(
            f"**Broadcasted Message In {sent} Chats.**"
        )
    except:
        pass
