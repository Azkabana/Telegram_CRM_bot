from aiogram import Router, types
from aiogram.filters import Command
import os

# from datetime import datetime
from dotenv import load_dotenv
from db.queries import db_find_username, db_find_idnoti, db_find_az


load_dotenv()
router = Router()
CHAT_ADMIN_ID = os.getenv("CHAT_ADMIN_ID")


# /find
@router.message(Command("find"))
async def handler_find(msg: types.Message):
    # Проверка на то что комнда /find - не пустая
    if msg.from_user.id != int(CHAT_ADMIN_ID) or len(msg.text.split(" ", 1)) < 2:
        await msg.answer(f"Что-то пошло не так...\nПример: /find @МарияГрозная")
        return
    find_it = msg.text.split(" ", 1)[1]
    pool = msg.bot.pool
    # обработка /find @...
    if find_it.startswith("@"):
        list_answer1 = await db_find_username(pool, find_it[1:])
        if not list_answer1:
            await msg.answer("Имя не найдено!")
            return
        else:
            for i in list_answer1:
                str_time = i[3].strftime("Дата регистрации: %d.%m.%Y [%H:%M]")
                await msg.answer(
                    f"Номер заявки: {i[0]}\n{i[1]}\nСтатус: {i[2]}\n{str_time}"
                )
        return
    # обработка /find 123...
    elif find_it.isdigit():
        i = await db_find_idnoti(pool, int(find_it))
        if not i:
            await msg.answer("Неверный номер заявки")
        else:
            str_time = i[3].strftime("Дата регистрации: %d.%m.%Y [%H:%M]")
            await msg.answer(
                f"Номер заявки: {i[0]}\n{i[1]}\nСтатус: {i[2]}\n{str_time}"
            )

    # обработка /find qweqwe...
    else:
        result = await db_find_az(pool, find_it)
        print(find_it)
        print(result)
        if not result:
            await msg.answer("Заявки с указанным текстом - отсуствует")
        else:
            for i in result:
                str_time = i[3].strftime("Дата регистрации: %d.%m.%Y [%H:%M]")
                await msg.answer(
                    f"Номер заявки: {i[0]}\n{i[1]}\nСтатус: {i[2]}\n{str_time}"
                )
