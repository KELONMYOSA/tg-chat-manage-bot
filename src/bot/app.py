import importlib
import pkgutil

from aiogram import Bot, Dispatcher

from src.bot import handlers
from src.config import settings

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


def init_bot():
    try:
        for x in pkgutil.iter_modules(handlers.__path__):
            handler = importlib.import_module("src.bot.handlers." + x.name)
            dp.include_router(handler.router)
    except Exception as e:
        print(e)


async def start_bot():
    print("The telegram bot has started!")
    while True:
        try:
            init_bot()
            await dp.start_polling(bot)
        except Exception as e:
            print(e)
