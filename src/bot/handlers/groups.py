from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.utils.auth import is_admin
from src.db.dao import Database

router = Router()


@router.message(Command("groups"))
async def cmd_admin(message: Message, state: FSMContext):
    await state.clear()
    if not await is_admin(message):
        return

    await message.delete()

    with Database() as db:
        groups_list = db.get_all_bot_groups()

    if groups_list:
        msg_text = "Список групп, в которых состоит бот:\n" + "\n".join(
            [f"- {group[1]} (id: {group[0]})" for group in groups_list]
        )
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="Проверить права", callback_data="checkPermissionsInGroups")
        await message.answer(text=msg_text, reply_markup=keyboard.as_markup())
    else:
        await message.answer(text="Список групп, в которых состоит бот, пуст!")


@router.callback_query(F.data == "checkPermissionsInGroups")
async def check_permissions_in_groups(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    if not await is_admin(call):
        return

    await call.answer()
    await call.message.delete()

    with Database() as db:
        groups_list = db.get_all_bot_groups()

    msg_rows = []
    for group in groups_list:
        bot_in_chat = await bot.get_chat_member(group[0], bot.id)
        msg_rows.append(f"- {group[1]} ({bot_in_chat.status.value})")

    await call.message.answer(text="Статус бота в группах (должен быть administrator):\n" + "\n".join(msg_rows))
