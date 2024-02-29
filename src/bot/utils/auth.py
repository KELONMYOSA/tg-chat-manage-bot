from aiogram.types import CallbackQuery, Message

from src.db.dao import Database


async def is_admin(msg: Message | CallbackQuery) -> bool:
    with Database() as db:
        if db.is_admin(msg.from_user.username):
            return True
        else:
            await msg.delete()
            await msg.answer(text="Вы не являетесь администратором!")
            return False
