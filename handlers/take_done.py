from aiogram import Router, types
from aiogram.filters import Command
from db.queries import db_status_take, db_status_done

router = Router()


# Взять заявку /take
@router.message(Command("take"))
async def handler_take(msg: types.Message):
    text = msg.text.split()
    if text[1].isdigit():
        await msg.answer(f"Заявка [{text[1]}]: Принято")
        pool = msg.bot.pool
        await db_status_take(pool, msg.from_user.id, int(text[1]), status="take")
    else:
        await msg.answer("после /take пробел и номер заявки")


# Закрыть заявку /done
@router.message(Command("done"))
async def handler_done(msg: types.Message):
    text = msg.text.split()
    if text[1].isdigit():
        await msg.answer(f"Заявка [{text[1]}]: Заркыто")
        pool = msg.bot.pool
        await db_status_done(pool, msg.from_user.id, int(text[1]), status="done")
    else:
        await msg.answer("после /done пробел и номер заявки")
