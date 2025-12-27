from aiogram import Router, types, F
import os
from dotenv import load_dotenv
from db.queries import db_re_idnoti, db_d_add
from bot import bot

load_dotenv()
router = Router()
CHAT_ADMIN_ID = os.getenv("CHAT_ADMIN_ID")


# Слушатель "Ответ" на сообщение AI
@router.message(F.reply_to_message)
async def handler_reply(msg: types.Message):
    if msg.from_user.id != int(CHAT_ADMIN_ID):
        print("Нет прав, для команды [reply]")
        return
    else:
        pool = msg.bot.pool
        result = await db_re_idnoti(pool, msg.reply_to_message.message_id)
        await db_d_add(pool, result[0], msg.text, msg.message_id, role="admin")
        await bot.send_message(result[1], msg.text)
