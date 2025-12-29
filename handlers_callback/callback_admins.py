from aiogram import Router, F, types
from aiogram.types import CallbackQuery
from dotenv import load_dotenv
import os
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from db.queries import db_status_take
from keyboards.inline import kb_edit_NewNoti, kb_ModerNewNoti, kb_AIAnswer
from db.queries import db_d_add, db_message_text
from api_ai_bots.lmstudio import ai_gen_usertext


load_dotenv()
router = Router()

CHAT_ADMIN_ID = os.getenv("CHAT_ADMIN_ID")
CHAT_KO_GROUP_ID = os.getenv("CHAT_KO_GROUP_ID")


class ModerFSM(StatesGroup):
    answerToUser = State()
    closeNoti = State()


# Взять
@router.callback_query(F.data.startswith("data_all:"))
async def handler_take_callback(call: CallbackQuery):
    worker = call.from_user
    id_noti = int(call.data.split(":")[1])
    id_user = int(call.data.split(":")[2])
    pool = call.bot.pool
    await db_status_take(pool, worker.id, id_noti, "take")
    await call.message.edit_reply_markup(
        reply_markup=kb_edit_NewNoti(worker.first_name)
    )
    await call.bot.send_message(
        chat_id=worker.id,
        text=call.message.text,
        reply_markup=kb_ModerNewNoti(id_noti=id_noti, id_user=id_user),
    )


# Ответить
@router.callback_query(F.data.startswith("data_AnswerToUser"))  # ловим кнопку
async def handler_AnswerToUser(call: CallbackQuery, state: FSMContext):
    print("handler_AnswerToUser: Start...")
    await state.set_state(ModerFSM.answerToUser)  # создаем FSM
    print("handler_AnswerToUser: Переменные...")
    id_noti = int(call.data.split(":")[1])
    user_id = int(call.data.split(":")[2])
    print("handler_AnswerToUser: Обновление FSM даных...")
    await state.update_data(id_noti=id_noti, user_id=user_id)
    await call.answer()
    print("handler_AnswerToUser: True")


@router.message(ModerFSM.answerToUser)
async def handler_AnswerToUser_1(msg: types.Message, state: FSMContext):
    print("handler_AnswerToUser_1: Start...")
    if msg.from_user.id != int(CHAT_ADMIN_ID):
        print("Нет прав, для команды [reply]")
        return
    else:
        pool = msg.bot.pool
        print("handler_AnswerToUser_1: Присвоение FSM переменных...")
        s_data = await state.get_data()
        id_noti = s_data["id_noti"]
        user_id = s_data["user_id"]
        print(f"Отпавляю пользователю: {user_id} ...")
        await msg.bot.send_message(user_id, msg.text)
        print("handler_AnswerToUser_1: добавляю ответ в бд...")
        await db_d_add(pool, id_noti, msg.text, msg.message_id, "admin")
        await state.clear()
        print("handler_AnswerToUser_1: True")
    # result = await db_re_idnoti(pool, worker.message_id)
    # await db_d_add(pool, result[0], msg.text, msg.message_id, "admin")
    # await bot.send_message(result[1], msg.text)


# Закрыть
@router.callback_query(F.data.startswith("data_Close:"))  # ловим кнопку
async def handler_CloseNoti(call: CallbackQuery):
    print("handler_CloseNoti: Start...")
    pool = call.bot.pool
    worker_id = call.from_user.id
    id_noti = int(call.data.split(":")[1])
    await db_status_take(pool, worker_id, id_noti, "done")
    await call.message.edit_reply_markup(reply_markup=kb_close_NewNoti())
    await call.answer()
    print("handler_CloseNoti: True")


# AI ответ
@router.callback_query(F.data.startswith("data_aiAnswer:"))  # ловим кнопку
async def handler_AIAnswer(call: CallbackQuery):
    print("handler_AIAnswer: Start...")
    find_id = int(call.data.split(":")[1])
    id_user = call.from_user.id
    pool = call.bot.pool
    row = await db_message_text(pool, find_id)
    row1 = ""
    for i in row:
        row1 += f"\n{i[0] +": " + i[1]}"
    result = await ai_gen_usertext(row1)
    sent = await call.bot.send_message(
        chat_id=id_user,
        text=result,
        reply_markup=kb_AIAnswer(id_noti=find_id, id_user=id_user),
    )

    # добавляем ответ ai в бд
    await db_d_add(pool, find_id, result, str(sent.message_id), role="ai")
    await call.answer()
    print("handler_AIAnswer: True")
