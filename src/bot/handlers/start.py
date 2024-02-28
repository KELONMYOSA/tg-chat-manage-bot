from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.delete()
    await message.answer(
        text="Привет!\nЯ - бот для управления чатами компании Комфортел. "
        "Доступ к функциям есть только у администраторов."
    )
