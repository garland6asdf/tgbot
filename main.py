import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers import admin_handler, user_handler

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(user_handler.router)
dp.include_router(admin_handler.router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())