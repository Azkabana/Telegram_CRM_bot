from aiogram import types, Router
from aiogram.filters import Command
from db.queries import db_add_user

router = Router()


# хэндлер — реакция на /start.
# types.Message - это совсем необязательно, нужен только для самого редактора, что бы подсказать ему на каком языке пишу
@router.message(Command("start"))
async def handler_start(message: types.Message):
    await message.answer(
        f"Здравствуйте! Вы обратились в LTech.\nОпишите ваш запрос — мы скоро ответим 👋"
    )
    # await message.answer(f"{message.chat.id}")
    pool = message.bot.pool
    await db_add_user(pool, message.from_user.first_name, message.from_user.id)


# После того как /start, сохраняем юзера в базу
