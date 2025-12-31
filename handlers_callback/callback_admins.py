from aiogram import Router, F, types
from aiogram.types import CallbackQuery
from dotenv import load_dotenv
import os
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from db.queries import db_status_take, db_message_text
from keyboards.inline import (
    kb_edit_NewNoti,
    kb_ModerNewNoti,
    kb_AIAnswer,
    kb_close_NewNoti,
    kb_NotiCloseOrleave,
)
from db.queries import db_d_add, db_message_text, db_status_done
from api_ai_bots.lmstudio import ai_gen_usertext


load_dotenv()
router = Router()

CHAT_ADMIN_ID = os.getenv("CHAT_ADMIN_ID")
CHAT_KO_GROUP_ID = os.getenv("CHAT_KO_GROUP_ID")


# Состояния
class ModerFSM(StatesGroup):
    answerToUser = State()  # Новое уведмомление модеру
    answerToUser_Conf = State()
    closeNoti = State()  # закрываем заявку
    AI1 = State()


# any --> Взять
@router.callback_query(F.data.startswith("data_all:"))
async def handler_take_callback(call: CallbackQuery):
    worker = call.from_user
    id_noti = int(call.data.split(":")[2])
    id_user = int(call.data.split(":")[1])
    print(id_noti)
    print(id_user)
    time = str(*call.data.split(":")[4:])
    pool = call.bot.pool
    await db_status_take(pool, worker.id, id_noti, "take")
    await call.message.edit_reply_markup(
        reply_markup=kb_edit_NewNoti(worker.first_name)
    )

    # Вытаскиваем последние сообщения пользователя
    row = await db_message_text(pool, id_noti)
    row1 = f"🆕 Новая заявка #{id_noti}\n👤 {call.from_user.first_name or 'нет'}\n🕒 {time}"
    for i in row:
        row1 += f"\n{i[1]}"

    await call.bot.send_message(
        chat_id=worker.id,
        text=row1,
        reply_markup=kb_ModerNewNoti(
            id_noti=id_noti, id_user=id_user, id_moder=worker.id
        ),
    )
    await call.answer()
    return


# --> Ответить
@router.callback_query(F.data.startswith("data_AnswerToUser"))  # ловим кнопку
async def handlerKB_AnswerToUser(call: CallbackQuery, state: FSMContext):
    print("handler_AnswerToUser: Start...")
    await state.set_state(ModerFSM.answerToUser)  # создаем FSM \ меняем статус
    print("handler_AnswerToUser: Переменные...")
    print(call.data)
    id_noti = int(call.data.split(":")[3])
    id_user = int(call.data.split(":")[1])
    print("handler_AnswerToUser: Обновление FSM даных...")
    await state.update_data(id_noti=id_noti, id_user=id_user)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()
    print("handler_AnswerToUser: True")
    return


# Собщение отправки
@router.message(ModerFSM.answerToUser)
async def handlerKB_AnswerToUser_1(msg: types.Message, state: FSMContext):
    print("handler_AnswerToUser_1: Start...")
    if msg.from_user.id != int(CHAT_ADMIN_ID):
        print("Нет прав, для команды [reply]")
        return
    else:
        pool = msg.bot.pool
        print("handler_AnswerToUser_1: Присвоение FSM переменных...")
        s_data = await state.get_data()
        print(s_data)
        id_noti = s_data["id_noti"]
        id_user = s_data["id_user"]
        await msg.bot.send_message(id_user, msg.text)
        await db_d_add(pool, id_noti, msg.text, msg.message_id, "admin")
        await msg.bot.send_message(
            chat_id=msg.from_user.id,
            text=f"Закрыть заявку #{id_noti} ?",
            reply_markup=kb_NotiCloseOrleave(id_noti),
        )
        await state.set_state(ModerFSM.answerToUser_Conf)  # меняем статус
        print("handler_AnswerToUser_1: True")
        return


# Подтверждение оставить заявку ? (Удалить сообщение)
@router.callback_query(F.data.startswith("data_NotiLeave:"))
async def handlerKB_LeaveNooti_Conf(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.clear()
    return


# Подтверждение закрыть заявку ? (Удалить сообщение)
@router.callback_query(F.data.startswith("data_NotiClose:"))
async def handlerKB_CloseNoti_Conf(call: CallbackQuery, state: FSMContext):
    pool = call.bot.pool
    id_noti = int(call.data.split(":")[1])
    await db_status_done(pool, call.from_user.id, id_noti, "done")
    await call.message.delete()
    await state.clear()
    return


# Закрыть
@router.callback_query(F.data.startswith("data_Close:"))  # ловим кнопку
async def handlerKB_CloseNoti(call: CallbackQuery):
    print("handler_CloseNoti: Start...")
    pool = call.bot.pool
    worker_id = call.from_user.id
    id_noti = int(call.data.split(":")[3])
    await db_status_take(pool, worker_id, id_noti, "done")
    await call.message.edit_reply_markup(reply_markup=kb_close_NewNoti())
    await call.answer()
    print("handler_CloseNoti: True")
    return


# AI ответ --> Отправить | Редактировать
@router.callback_query(F.data.startswith("data_aiAnswer:"))  # ловим кнопку
async def handlerKB_AIAnswer(call: CallbackQuery, state: FSMContext):
    print("handlerKB_AIAnswer: Start...")
    find_id = int(call.data.split(":")[3])
    id_user = int(call.data.split(":")[1])
    pool = call.bot.pool

    row = await db_message_text(pool, find_id)
    row1 = ""
    for i in row:
        row1 += f"\n{i[0] +": " + i[1]}"
    result = await ai_gen_usertext(row1)
    print("Собираюсь отправить Сгенерированное сообщение модеру")

    sent = await call.bot.send_message(
        chat_id=call.from_user.id,
        text=result,
        reply_markup=kb_AIAnswer(id_user=id_user, id_noti=find_id),
    )
    # сохраняем текст в FSM
    await state.set_state(ModerFSM.AI1)
    await state.update_data(ai_text=result)

    # добавляем ответ ai в бд
    await db_d_add(pool, find_id, result, str(sent.message_id), role="ai")

    # Закрываем кнопки
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()
    print("handlerKB_AIAnswer: True")
    return


# Отправить | Редактировать --> Редактировать
@router.callback_query(F.data.startswith("data_EditAIAswer:"))
async def handlerKB_EditAIAnswer(call: CallbackQuery, state: FSMContext):
    await state.clear()  # Закрыть старый FSM
    await handlerKB_AnswerToUser(
        call, state
    )  # Открвается новый FSM # data_EditAIAswer: - должна иметь
    # id_noti, id_user
    return


# Отправить | Редактировать --> Отправитьf
@router.callback_query(F.data.startswith("data_CallMsg:"))
async def handlerKB_EAiA_Answer(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    id_user = call.data.split(":")[1]
    id_noti = call.data.split(":")[3]
    ai_text = data["ai_text"]
    await call.bot.send_message(chat_id=id_user, text=ai_text)
    await call.message.edit_reply_markup(reply_markup=None)
    await state.clear()

    # Новое состояние для подтверждения статуса заявки
    await state.set_state(ModerFSM.answerToUser_Conf)
    await call.bot.send_message(
        chat_id=call.from_user.id,
        text=f"Закрыть заявку #{id_noti} ?",
        reply_markup=kb_NotiCloseOrleave(id_noti),
    )
    return
