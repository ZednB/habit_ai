import os

from aiogram import Bot, Dispatcher, types
import requests
from aiogram.filters import Command

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
API_URL = 'http://127.0.0.1:8000'

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def start_handler(message: types.Message):
    chat_id = message.chat.id
    args = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
    if args:
        email = args
        requests.post(f"{API_URL}/users/link-telegram", params={'email': email, 'chat_id': chat_id})
    await message.answer("Привет! Я буду присылать тебе напоминания 🚀")


# async def main():
#     await dp.start_polling(bot)


async def send_telegram_notification(chat_id: int, text: str):
    await bot.send_message(chat_id=chat_id, text=text)
