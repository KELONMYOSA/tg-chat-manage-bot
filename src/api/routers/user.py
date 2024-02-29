from fastapi import APIRouter

from src.bot.app import bot
from src.db.dao import Database

router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.post("/remove/{user_id}")
async def remove_user(user_id: int):
    with Database() as db:
        groups_list = db.get_all_bot_groups()

    removed_from = []
    for group in groups_list:
        try:
            await bot.ban_chat_member(group[0], user_id)
            removed_from.append(group[0])
        except:  # noqa: E722
            pass
    return {"groupsRemovedFrom": removed_from}
