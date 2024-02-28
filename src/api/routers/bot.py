from fastapi import APIRouter, HTTPException

from src.bot.app import bot

router = APIRouter(
    prefix="/bot",
    tags=["Bot"],
)


@router.get("/health")
async def health_check():
    try:
        bot_info = await bot.get_me()
        return {"status": "ok", "bot": bot_info.username}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))  # noqa: B904
