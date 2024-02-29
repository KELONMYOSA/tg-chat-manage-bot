from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import LinkPreviewOptions, Message

from src.bot.utils.auth import is_admin
from src.db.dao import Database

router = Router()


@router.message(Command("user_add"))
async def cmd_user_add(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    if not await is_admin(message):
        return

    await message.delete()

    with Database() as db:
        groups_list = db.get_all_bot_groups()

    if not groups_list:
        await message.answer(text="Список групп, в которых состоит бот, пуст!")
        return

    msg_rows = []
    for group in groups_list:
        try:
            link = await bot.create_chat_invite_link(group[0], member_limit=1)
            msg_rows.append(f"{group[1]}: {link.invite_link}")
        except:  # noqa: E722
            pass

    await message.answer(
        text="Ссылки для присоединения к группам:\n" + "\n".join(msg_rows),
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )
