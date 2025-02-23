import asyncio
import logging

import aiogram 
import aiogram.enums
import aiogram.fsm
import aiogram.types
# import handlers

import secret_data

import handlers


async def main():
    bot = aiogram.Bot(token=secret_data.BOT_TOKEN, default=aiogram.client.bot.DefaultBotProperties(parse_mode=aiogram.enums.ParseMode.HTML))
    dp = aiogram.Dispatcher(storage=aiogram.fsm.storage.memory.MemoryStorage())
    dp.include_router(handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())







