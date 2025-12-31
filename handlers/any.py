import os
from aiogram import types, Router

# from aiogram.filters import Command
from dotenv import load_dotenv
from db.queries import db_add_ticket, db_status_noti, db_d_add
from keyboards.inline import kb_take_request, kb_ModerNewNoti
from bot import bot

load_dotenv()
router = Router()
CHAT_ADMIN_ID = os.getenv("CHAT_ADMIN_ID")
CHAT_KO_GROUP_ID = os.getenv("CHAT_KO_GROUP_ID")


@router.message()
async def handler_any(message: types.Message):
    if message.from_user.id != int(CHAT_ADMIN_ID):
        pool = message.bot.pool
        # result_status[0] - номер заявки result_status[1] - статус
        result_status = await db_status_noti(pool, message.from_user.id)
        print(f"result_status: {result_status}")

        # безопастная обработка статуса
        if result_status == None:
            print("if result_status == None: start...")

            # Добавляем заявку в бд
            await db_add_ticket(pool, message.from_user.id, message.text)
            print("db_add_ticket: True")

            result_status2 = await db_status_noti(pool, message.from_user.id)
            ticket_id2 = result_status2[0]
            str_time2 = result_status2[3].strftime("%H:%M - %d.%m.%Y")
            notification2 = f"🆕 Новая заявка #{result_status2[0]}\n👤 {message.from_user.first_name or 'нет'}\n🕒 {str_time2}\n\n{message.text}"
            print("Переменные: True")

            await db_d_add(pool, ticket_id2, message.text, message.message_id, "user")
            print("db_d_add: True")

            print(f"Предеаю время в клаву: {str_time2}")
            print(f"Класс вермени: {type(str_time2)}")
            await message.bot.send_message(
                CHAT_KO_GROUP_ID,
                notification2,
                reply_markup=kb_take_request(
                    id_noti=ticket_id2, id_user=message.from_user.id, time=str_time2
                ),
            )
            print("if result_status == None: True")
            return
        else:
            # Переменный для услвоий
            ticket_id = result_status[0]
            worker_id = result_status[2]
            str_time = result_status[3].strftime("%H:%M - %d.%m.%Y")
            notification = f"🆕 Новая заявка #{result_status[0]}\n👤 {message.from_user.first_name or 'нет'}\n🕒 {str_time}\n\n{message.text}"

            # Продолжение заявки если статус не done.
            if result_status[1] != "done":
                if result_status[1] == "take":
                    await db_d_add(
                        pool, ticket_id, message.text, message.message_id, "user"
                    )
                    notification_take = f"👤 {message.from_user.first_name}\nЗаявка #{ticket_id}\n\n{message.text}"
                    await message.bot.send_message(
                        worker_id,
                        notification_take,
                        reply_markup=kb_ModerNewNoti(
                            id_noti=ticket_id, id_user=message.from_user.id
                        ),
                    )
                    return

                # Нужно просто изменить сообщзение - не сделанно
                elif result_status[1] == "new":
                    await db_d_add(
                        pool, ticket_id, message.text, message.message_id, "user"
                    )
                    return

            # Создание новой заявки со статусом new
            else:
                await db_add_ticket(pool, message.from_user.id, message.text)
                await db_d_add(
                    pool, ticket_id, message.text, message.message_id, "user"
                )
                await message.bot.send_message(
                    CHAT_KO_GROUP_ID,
                    notification,
                    reply_markup=kb_take_request(
                        id_noti=ticket_id, id_user=message.from_user.id
                    ),
                )
                await message.answer("Заявка отправлена ✅")
                return
    else:
        print("Модер случайно написал в чат")
        return
