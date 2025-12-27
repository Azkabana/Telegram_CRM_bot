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
    print("result_status - получил None")
    print(f"result_status = {result_status}")
    # безопастная обработка статуса
    if result_status == None:
        print("if result_status is None: - прошли")
        await db_add_ticket(pool, message.from_user.id, message.text)
        await db_d_add(pool, ticket_id, message.text, message.message_id, role="user")
        await bot.send_message(CHAT_ADMIN_ID, notification)
        return
    else:
        notification = f"Новая заявка!\nПользователь: {message.from_user.first_name or 'нет'}\nID заявки: {result_status[0]}\n\n{message.text}"
        ticket_id = result_status[0]
        worker_id = result_status[2]
        # Продолжение заявки если статус не done.
        if result_status[1] != "done":
            if result_status[1] == "take":
                await db_d_add(
                    pool, ticket_id, message.text, message.message_id, "user"
                )
                notification_take = f"От: {message.from_user.first_name}\nПо завявке: {ticket_id}\n\n{message.text}"
                await bot.send_message(worker_id, notification_take)
                return
            if result_status[1] == "new":
                await db_d_add(
                    pool, ticket_id, message.text, message.message_id, role="user"
                )
                await bot.send_message(CHAT_ADMIN_ID, notification)
                return
        # Создание новой заявки со статусом new
        else:
            await db_add_ticket(pool, message.from_user.id, message.text)
            await db_d_add(
                pool, ticket_id, message.text, message.message_id, role="user"
            )
            await bot.send_message(CHAT_ADMIN_ID, notification)
            await message.answer("Заявка отправлена ✅")
            return
