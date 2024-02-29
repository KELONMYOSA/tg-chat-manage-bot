from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.utils.auth import is_admin
from src.bot.utils.states import StatesMachine
from src.db.dao import Database

router = Router()


@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext):
    await state.clear()
    if not await is_admin(message):
        return

    await message.delete()

    with Database() as db:
        admin_list = db.get_all_admins()

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Добавить", callback_data="addAdmin")

    if admin_list:
        msg_text = "Список администраторов:\n" + "\n".join([f"- @{admin}" for admin in admin_list])
        keyboard.button(text="Удалить", callback_data="removeAdmin")
    else:
        msg_text = "Список администраторов пуст!"

    await message.answer(text=msg_text, reply_markup=keyboard.as_markup())


@router.callback_query(F.data == "addAdmin")
async def add_admin(call: CallbackQuery, state: FSMContext):
    await state.clear()
    if not await is_admin(call):
        return

    await call.answer()
    await call.message.delete()

    await call.message.answer(text="Отправьте имя пользователя:")
    await state.set_state(StatesMachine.get_admin_username)


@router.message(StatesMachine.get_admin_username)
async def get_admin_username(message: Message, state: FSMContext):
    await state.clear()
    if not await is_admin(message):
        return

    username = message.text
    if username.startswith("@"):
        username = username[1:]
    elif username.startswith("https://t.me/"):
        username = username[13:]

    with Database() as db:
        db.add_admin(username)

    await message.answer(text=f"Администратор @{username} был добавлен")


@router.callback_query(F.data == "removeAdmin")
async def remove_admin(call: CallbackQuery, state: FSMContext):
    await state.clear()
    if not await is_admin(call):
        return

    await call.answer()
    await call.message.delete()

    with Database() as db:
        admin_list = db.get_all_admins()

    if len(admin_list) > 1:
        keyboard = InlineKeyboardBuilder()
        for admin in admin_list:
            keyboard.row(InlineKeyboardButton(text=admin, callback_data=f"removeAdmin_|_{admin}"))
        keyboard.row(InlineKeyboardButton(text="Отмена", callback_data="removeAdminCancel"))
        await call.message.answer(text="Выберите администратора для удаления:", reply_markup=keyboard.as_markup())
    else:
        await call.message.answer(text="Нельзя удалить последнего администратора!")


@router.callback_query(F.data.startswith("removeAdmin_|_"))
async def remove_admin_select(call: CallbackQuery, state: FSMContext):
    await state.clear()
    if not await is_admin(call):
        return

    await call.answer()
    await call.message.delete()

    username = call.data.split("_|_")[1]

    with Database() as db:
        db.remove_admin(username)

    await call.message.answer(text=f"Администратор @{username} был удален")


@router.callback_query(F.data == "removeAdminCancel")
async def remove_admin_cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    if not await is_admin(call):
        return

    await call.answer()
    await call.message.delete()
