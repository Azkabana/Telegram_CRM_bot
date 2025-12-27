from aiogram import Router, types
import os
from aiogram.filters import Command
from dotenv import load_dotenv
from db.queries import db_message_text, db_d_add
from api_ai_bots.lmstudio import ai_gen_usertext

# from bot import bot

load_dotenv()
CHAT_ADMIN_ID = os.getenv("CHAT_ADMIN_ID")
router = Router()


# /ai 123, комнда для модеров - получают генерацию ответа на заявку
@router.message(Command("ai"))
async def ai_answer(msg: types.Message):
    # Проверка на то что комнда /find - не пустая
    if msg.from_user.id != int(CHAT_ADMIN_ID) or len(msg.text.split(" ", 1)) < 2:
        await msg.answer(f"Что-то пошло не так...\nПример: /ai 123")
        return
    find_id = int(msg.text.split(" ", 1)[1])
    pool = msg.bot.pool
    row = await db_message_text(pool, find_id)
    row1 = ""
    for i in row:
        row1 += f"\n{i[0] +": " + i[1]}"
    result = await ai_gen_usertext(row1)
    sent = await msg.answer(result)
    # добавляем ответ ai в бд
    await db_d_add(pool, find_id, result, str(sent.message_id), role="ai")