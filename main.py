from aiogram import Bot, Dispatcher
from handlers import user_handler, admin_handler
from cfg import TOKEN
from handlers import admin_handler, user_handler
bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(user_handler.router)
dp.include_router(admin_handler.router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())