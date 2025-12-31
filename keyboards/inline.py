from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Уведомление в чат модеров
def kb_take_request(id_user: int = None, id_noti: int = None, time: str = None):
    kb = InlineKeyboardBuilder()
    data_all = f"data_all:{id_user}:{id_noti}:{time}"
    kb.button(text="🟢 Взять", callback_data=data_all)
    return kb.as_markup()


# Взять
def kb_edit_NewNoti(worker_name: str):
    kb = InlineKeyboardBuilder()
    kb.button(text=f"✅ Взял(а) {worker_name}", callback_data="take:")
    return kb.as_markup()


# Уведомление модеру
def kb_ModerNewNoti(id_user: int = None, id_moder: int = None, id_noti: int = None):
    kb = InlineKeyboardBuilder()
    data_AnswerToUser = f"data_AnswerToUser:{id_user}:{id_moder}:{id_noti}"  # Ответить
    data_Close = f"data_Close:{id_user}:{id_moder}:{id_noti}"  # Закрыть
    data_aiAnswer = f"data_aiAnswer:{id_user}:{id_moder}:{id_noti}"  # AI ответ
    kb.button(text=f"Ответить", callback_data=data_AnswerToUser)
    kb.button(text=f"AI Ответ", callback_data=data_aiAnswer)
    kb.button(text=f"Закрыть", callback_data=data_Close)
    kb.adjust(2)
    return kb.as_markup()


# --> Отправить | Редактировать
def kb_AIAnswer(id_user: int = None, id_moder: int = None, id_noti: int = None):
    kb = InlineKeyboardBuilder()
    data_CallMsg = f"data_CallMsg:{id_user}:{id_moder}:{id_noti}"
    data_EditAIAswer = f"data_EditAIAswer:{id_user}:{id_moder}:{id_noti}"
    kb.button(text=f"Отправить", callback_data=data_CallMsg)
    kb.button(text=f"Редактировать ", callback_data=data_EditAIAswer)
    kb.adjust(2)
    return kb.as_markup()


# --> Отсавить | Закрыть
def kb_NotiCloseOrleave(id_noti):
    kb = InlineKeyboardBuilder()
    kb.button(text="Оставить", callback_data="data_NotiLeave:")
    kb.button(text="Закрыть", callback_data=f"data_NotiClose:{id_noti}")
    kb.adjust(2)
    return kb.as_markup()


# Закрыть
def kb_close_NewNoti():
    kb = InlineKeyboardBuilder()
    kb.button(text=f"✅ Закрыто", callback_data="closed")
    return kb.as_markup()
