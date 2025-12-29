from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Уведомление в чат модеров
def kb_take_request(id_noti: int, id_user: int):
    kb = InlineKeyboardBuilder()
    data_all = f"data_all:{id_noti}:{id_user}"
    kb.button(text="🟢 Взять", callback_data=data_all)
    return kb.as_markup()


# Взять
def kb_edit_NewNoti(worker_name: str):
    kb = InlineKeyboardBuilder()
    kb.button(text=f"✅ Взял(а) {worker_name}", callback_data="take:")
    return kb.as_markup()


# Закрыть
def kb_close_NewNoti():
    kb = InlineKeyboardBuilder()
    kb.button(text=f"✅ Закрыто", callback_data="closed")
    return kb.as_markup()


# Уведомление модеру
def kb_ModerNewNoti(id_noti, id_user):
    kb = InlineKeyboardBuilder()
    data_AnswerToUser = f"data_AnswerToUser:{id_noti}:{id_user}"  # Ответить
    data_Close = f"data_Close:{id_noti}:{id_user}"  # Закрыть
    data_aiAnswer = f"data_aiAnswer:{id_noti}:{id_user}"  # AI ответ
    kb.button(text=f"Ответить", callback_data=data_AnswerToUser)
    kb.button(text=f"AI Ответ", callback_data=data_aiAnswer)
    kb.button(text=f"Закрыть", callback_data=data_Close)
    kb.adjust(2)
    return kb.as_markup()


# Ответ\Редакт Ai соощения
def kb_AIAnswer(id_noti, id_user):
    kb = InlineKeyboardBuilder()
    data_CallMsg = f"data_CallMsg:{id_noti}:{id_user}"
    data_EditMsg = f"data_EditMsg:{id_noti}:{id_user}"
    kb.button(text=f"Отправить", callback_data=data_CallMsg)
    kb.button(text=f"Редактировать ", callback_data=data_EditMsg)
    kb.adjust(2)
    return kb.as_markup()
