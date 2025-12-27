from aiogram import Router, types
from aiogram.filters import Command
from db.queries import db_status_take, db_status_done

router = Router()


# Взять заявку /take
@router.message(Command("take"))
async def handler_take(msg: types.Message):
    text = msg.text.split()
    if text[1].isdigit():
        await msg.answer("take прошел")
        pool = msg.bot.pool
        await db_status_take(pool, int(text[1]))
    else:
        await msg.answer("после /take пробел и номер заявки")


# Закрыть заявку /done
@router.message(Command("done"))
async def handler_done(msg: types.Message):
    text = msg.text.split()
    if text[1].isdigit():
        await msg.answer("done прошел")
        pool = msg.bot.pool
        await db_status_done(pool, int(text[1]))
    else:
        await msg.answer("после /done пробел и номер заявки")
