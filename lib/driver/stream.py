import os
import asyncio
from pytgcalls import GroupCallFactory
from pyrogram import Client, filters
from lib.driver.misc import VIDEO_CALL, CHANNEL_VIDEO
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from lib.config import API_ID, API_HASH, SESSION_NAME

app = Client(SESSION_NAME, API_ID, API_HASH)
group_call_factory = GroupCallFactory(app, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM)

@Client.on_message(filters.cmd("stream"))
async def stream(client, m: Message):
    replied = m.reply_to_message
    if not replied:
        if len(m.command) < 2:
            await m.reply("`Reply to some Video or Give Some Live Stream Url!`")
        else:
            livelink = m.text.split(None, 1)[1]
            msg = await m.reply("`Starting Live Stream...`")
            chat_id = m.chat.id
            user = m.from_user.mention
            await asyncio.sleep(1)
            try:
                group_call = group_call_factory.get_group_call()
                await group_call.join(chat_id)
                await group_call.start_video(livelink)
                VIDEO_CALL[chat_id] = group_call
                await msg.delete()
                keyboard = InlineKeyboardMarkup(

                    [
                        [
                            InlineKeyboardButton(
                                '📣 Channel support', url='https://t.me/feyystatus',
                            ),
                        ],
                    ],
                )
                await m.reply_photo(
                    photo="./etc/banner.png",
                    caption=f"**Started [Live Streaming](livelink) !**\n**Request by:** {user}\n**To stop:** /stop",
                    reply_markup=keyboard,
                )

            except Exception as e:
                await msg.edit(f"**Error** -- `{e}`")
    elif replied.video or replied.document:
        msg = await m.reply("`Downloading...`")
        video = await client.download_media(m.reply_to_message)
        chat_id = m.chat.id
        user = m.from_user.mention
        await asyncio.sleep(2)
        try:
            group_call = group_call_factory.get_group_call()
            await group_call.join(chat_id)
            await group_call.start_video(video)
            VIDEO_CALL[chat_id] = group_call
            await msg.delete()
            keyboard = InlineKeyboardMarkup(

                [
                    [
                        InlineKeyboardButton(
                            '📣 Channel support', url='https://t.me/feyystatus',
                        ),
                    ],
                 ],
             )
            await m.reply_photo(
                photo="./etc/banner.png",
                caption=f"**Streamed video from telegram files**\n**Requested by:** {user}\n**To stop:** /stop",
                reply_markup=keyboard,
            )
        except Exception as e:
            await msg.edit(f"**Error** -- `{e}`")
    else:
        await m.reply("`Reply to some Video!`")

@Client.on_message(filters.cmd("cstream"))
async def cstream(client, m: Message):
    replied = m.reply_to_message
    if not replied:
        if len(m.command) < 2:
            await m.reply("`Reply to some Video or Give Some Live Stream Url!`")
        else:
            livelink = m.text.split(None, 1)[1]
            msg = await m.reply("`Starting Live Stream...`")
            chat_id = m.chat.title
            user = m.from_user.mention
            await asyncio.sleep(1)
            try:
                group_call = group_call_factory.get_group_call()
                await group_call.join(int(chat_id))
                await group_call.start_video(livelink)
                CHANNEL_VIDEO[chat_id] = group_call
                await msg.delete()
                keyboard = InlineKeyboardMarkup(

                    [
                        [
                            InlineKeyboardButton(
                                '📣 Channel support', url='https://t.me/feyystatus',
                            ),
                        ],
                    ],
                )
                await m.reply_photo(
                    photo="./etc/banner.png",
                    caption=f"**Started [Live Streaming](livelink) !**\n**Request by:** {user}\n**To stop:** /stop",
                    reply_markup=keyboard,
                )

            except Exception as e:
                await msg.edit(f"**Error** -- `{e}`")
    elif replied.video or replied.document:
        msg = await m.reply("`Downloading...`")
        video = await client.download_media(m.reply_to_message)
        chat_id = m.chat.title
        user = m.from_user.mention
        await asyncio.sleep(2)
        try:
            group_call = group_call_factory.get_group_call()
            await group_call.join(int(chat_id))
            await group_call.start_video(video)
            CHANNEL_VIDEO[chat_id] = group_call
            await msg.delete()
            keyboard = InlineKeyboardMarkup(

                [
                    [
                        InlineKeyboardButton(
                            '📣 Channel support', url='https://t.me/feyystatus',
                        ),
                    ],
                 ],
             )
            await m.reply_photo(
                photo="./etc/banner.png",
                caption=f"**Streamed video from telegram files**\n**Requested by:** {user}\n**To stop:** /cstop",
                reply_markup=keyboard,
            )
        except Exception as e:
            await msg.edit(f"**Error** -- `{e}`")
    else:
        await m.reply("`Reply to some Video!`")
