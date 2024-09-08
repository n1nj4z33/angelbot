import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from app.handlers import router
from aiohttp import web

logging.basicConfig(level=logging.INFO)


load_dotenv()

bot = Bot(token=os.getenv("API_TOKEN"))

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать"),
    ]
    await bot.set_my_commands(commands)


#TODO move to handlers.py
async def handle(request):
    data = await request.json()
    text = f"Результаты опроса:\n{data}"
    await bot.send_message(
        chat_id=os.getenv("GROUP_CHAT_ID"),
        message_thread_id=os.getenv("MESSAGE_THREAD_ID"),
        text=text
    )
    return web.Response(text="Данные отправлены в Telegram канал!")

async def main():


    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await set_commands(bot)
    
    app = web.Application()
    app.add_routes([web.post('/submit', handle)])  # добавляем маршрут для обработки POST запросов
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)  # Запуск веб-сервера на localhost:8080
    await site.start()

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")