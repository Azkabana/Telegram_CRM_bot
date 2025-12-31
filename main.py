# Этот проект связан с GitHub
import asyncio
from bot import dp, bot
from db.base import create_pool, setup_table
from handlers.start import router as handler_start

from handlers.find import router as find
from handlers.reply import router as reply
from handlers_callback.callback_admins import router as callback_admins
from handlers.any import router as handler_any


dp.include_router(handler_start)
dp.include_router(find)
dp.include_router(reply)
dp.include_router(callback_admins)
dp.include_router(handler_any)  # Эта регистрациядолжна быть ниже всехё
# либо он закроет все ханделры что пойдут ниже, потому что она уневерсальная


# Это главный холл гильдии, это не цикл
async def main():
    print("Вечный цикл обработки обновлений: True")
    pool = await create_pool()
    bot.pool = pool
    await setup_table(pool)  # vсоздаем таблицы 1 раз, при запуске бота
    # Вот ниже, это реально бесконечный цикл обновлений, который слушает телегу
    await dp.start_polling(bot)


# точка входа, запускает main(), только если он запущен руками, а не импортом, по сути не обязательноые строки.
if __name__ == "__main__":
    print('Условие [if __name__ == "__main__"]: True ')
    asyncio.run(main())

# Note-info
# Bot
# Управляет отправкой/приёмом сообщений через Telegram API.

# Dispatcher
# Хранит все правила (хэндлеры), по которым решает:
# “пришло сообщение — кому его передать?”

# Handlers
# Функции, которые вызываются, когда пришло подходящее событие.
# Например: команда /start, текст, кнопка, колбэк.

# Polling
# Механизм, который телеграму говорит:
# “дай мне новые обновления”
# И сразу же их обрабатывает.

# Новый проект для апргрейда в ооп
# project_bot_3
