import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

# грузим .env и вытаскиваем токен
load_dotenv()
TOKEN = os.getenv("API_TOKEN")

# создаём объекты: сам бот и диспетчер, который будет ловить сообщения.
bot = Bot(TOKEN)  # Обект бот
# dp — это Dispatcher из aiogram.
# Он хранит все хэндлеры и решает, какой хэндлер вызвать, когда приходит сообщение или команда.
dp = Dispatcher()  # Обьект диспетчер,
