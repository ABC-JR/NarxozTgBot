import asyncio
import logging
from aiogram import Bot, Dispatcher, types

from aiogram.fsm.storage.memory import MemoryStorage

from aiogram.fsm.state import State, StatesGroup
from app.handler import router

API_TOKEN = "8198728804:AAFpmPJ820ZVGVgc5LBS_IHnbjkcpPoV6oo"
CHANNEL_ID = "-4583360988"

# Main function to start polling
async def main():


    bot = Bot(token=API_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())