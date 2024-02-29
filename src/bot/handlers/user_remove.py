from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.utils.auth import is_admin
from src.bot.utils.states import StatesMachine
from src.db.dao import Database

router = Router()


@router.message(Command("user_remove"))
async def cmd_user_remove(message: Message, state: FSMContext):
    await state.clear()
    if not await is_admin(message):
        return

    await message.delete()
    await message.answer(text="Отправьте id пользователя для удаления или перешлите его сообщение:")
    await state.set_state(StatesMachine.get_user_id_to_remove)


@router.message(StatesMachine.get_user_id_to_remove)
async def get_user_id_to_remove(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    if not await is_admin(message):
        return

    if message.forward_from:
        user_id = message.forward_from.id
    else:
        try:
            user_id = int(message.text)
        except:  # noqa: E722
            await message.answer("Введен некорректный id пользователя!")
            return

    with Database() as db:
        groups_list = db.get_all_bot_groups()

    if not groups_list:
        await message.answer(text="Список групп, в которых состоит бот, пуст!")
        return

    msg_rows = []
    for group in groups_list:
        try:
            await bot.ban_chat_member(group[0], user_id)
            msg_rows.append(f"{group[1]}: Удален")
        except:  # noqa: E722
            msg_rows.append(f"{group[1]}: Не удален")

    await message.answer(text="Статус удаления из групп:\n" + "\n".join(msg_rows))
