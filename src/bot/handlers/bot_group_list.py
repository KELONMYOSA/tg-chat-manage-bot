from aiogram import Bot, F, Router
from aiogram.enums import ContentType
from aiogram.types import Message

from src.db.dao import Database

router = Router()


@router.message(F.content_type == ContentType.NEW_CHAT_MEMBERS)
async def on_new_chat_members(message: Message, bot: Bot):
    if bot.id in [user.id for user in message.new_chat_members]:
        chat_id = message.chat.id
        title = message.chat.title
        with Database() as db:
            db.add_bot_group(chat_id, title)


@router.message(F.content_type == ContentType.LEFT_CHAT_MEMBER)
async def on_left_chat_member(message: Message, bot: Bot):
    if message.left_chat_member.id == bot.id:
        chat_id = message.chat.id
        with Database() as db:
            db.remove_bot_group(chat_id)
