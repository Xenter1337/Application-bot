from aiogram import Dispatcher, Bot
import asyncio
from config import TOKEN
from handlers.client import Rclient, db
from handlers.admin import router


async def main():
    global conn
    dp = Dispatcher()
    bot = Bot(TOKEN)
    dp.include_routers(Rclient, router)
    dp.shutdown.register(db.on_shut)
    
    await db.start_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())
    
