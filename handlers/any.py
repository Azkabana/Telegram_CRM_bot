import os
from aiogram import types, Router

# from aiogram.filters import Command
from dotenv import load_dotenv
from db.queries import db_add_ticket, db_ststus_noti, db_d_add
from bot import bot

load_dotenv()
router = Router()
CHAT_ADMIN_ID = os.getenv("CHAT_ADMIN_ID")


@router.message()
async def handler_any(message: types.Message):
    pool = message.bot.pool
    # result_status[0] - номер заявки result_status[1] - статус
    result_status = await db_ststus_noti(pool, message.from_user.id)
    ticket_id = result_status[0]
    text = message.text
    # Продолжение заявки если статус не done.
    if result_status[1] != "done":
        await db_d_add(pool, ticket_id, text, message.message_id, role="user")
        return
    # Создание новой заявки со статусом new
    else:
        notification_id = await db_add_ticket(pool, message.from_user.id, message.text)
        notification = f"Новая заявка!\nUsername: @{message.from_user.username or 'нет'}\nТекст: {message.text}\nID в БД: {notification_id}"
        await bot.send_message(CHAT_ADMIN_ID, notification)
        await message.answer("Заявка отправлена ✅")
        return
