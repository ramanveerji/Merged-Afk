import asyncio
from typing import Union
from datetime import datetime, timedelta
from afk import cleanmode, app, botname
from afk.database import is_cleanmode_on
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time


async def put_cleanmode(chat_id, message_id):
    if chat_id not in cleanmode:
        cleanmode[chat_id] = []
    time_now = datetime.now()
    put = {
        "msg_id": message_id,
        "timer_after": time_now + timedelta(minutes=5),
    }
    cleanmode[chat_id].append(put)


async def auto_clean():
    while not await asyncio.sleep(30):
        try:
            for chat_id in cleanmode:
                if not await is_cleanmode_on(chat_id):
                    continue
                for x in cleanmode[chat_id]:
                    if datetime.now() > x["timer_after"]:
                        try:
                            await app.delete_messages(chat_id, x["msg_id"])
                        except FloodWait as e:
                            await asyncio.sleep(e.x)
                        except:
                            continue
                    else:
                        continue
        except:
            continue


asyncio.create_task(auto_clean())


RANDOM = [
    "https://graph.org/file/8b24e062af57ae509f46c.png",
    "https://graph.org/file/77c3d8f59bdba96aeb99c.png",
    "https://graph.org/file/9b5d2fc8956dc43707554.png",
    "https://graph.org/file/9f3e2925449592bb47e10.png",
    "https://graph.org/file/d44a746f29f1d648fff38.png",
    "https://graph.org/file/4541c9ae3930c61e09573.png",
    "https://graph.org/file/42b8b7fe024cb90c988da.png",
    "https://graph.org/file/0c169b9671a86f539f74a.png",
    "https://graph.org/file/d9c4498396ab4ec04f506.png",
    "https://graph.org/file/70755fd35c8930cfb17a6.png",
    "https://graph.org/file/513085d103b3aab965f13.png",
    "https://graph.org/file/98b69b39d38616871826b.png",
    "https://graph.org/file/556fecac5458b0cbdf11b.png",
    "https://graph.org/file/b810f7f8a238f58b3c0b2.png"
]


HELP_TEXT = f"""Welcome to {botname}'s Help Section.

- When someone mentions you in a chat, the user will be notified you are AFK. You can even provide a reason for going AFK, which will be provided to the user as well.


/afk - This will set you offline.

/afk [Reason] - This will set you offline with a reason.

/afk [Replied to a Sticker/Photo] - This will set you offline with an image or sticker.

/afk [Replied to a Sticker/Photo] [Reason] - This will set you afk with an image and reason both.

/settings - To change or edit basic settings of AFK Bot.
"""

def settings_markup(status: Union[bool, str] = None):
    buttons = [
        [
            InlineKeyboardButton(text="🔄 Clean Mode", callback_data="cleanmode_answer"),
            InlineKeyboardButton(
                text="✅ Enabled" if status == True else "❌ Disabled",
                callback_data="CLEANMODE",
            ),
        ],
        [
            InlineKeyboardButton(text="🗑 Close Menu", callback_data="close"),
        ],
    ]
    return buttons