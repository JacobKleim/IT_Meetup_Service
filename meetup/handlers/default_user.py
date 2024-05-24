import re

from telegram import Update
from telegram.ext import CallbackContext

from meetup.keyboards import (
    BACK_TO_MENU_KEYBOARD,
    SPEAKERS_EVENT_KEYBOARD,
    EVENT_KEYBOARD, EVENTS_KEYBOARD
)


def want_meet(update: Update, context: CallbackContext):
    update.callback_query.answer()
    update.callback_query.edit_message_text(text='Вы нажали "Хочу познакомиться".', reply_markup=BACK_TO_MENU_KEYBOARD)
    return "START"


def event_info(update: Update, context: CallbackContext):
    event_id = 'последнем'
    if re.match(r"^event\d+$", update.callback_query.data):
        event_id = update.callback_query.data.replace('event', '')

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=f'Информация о {event_id} мероприятии.', reply_markup=EVENT_KEYBOARD)
    return "EVENT"


def event_schedule(update: Update, context: CallbackContext):
    update.callback_query.answer()
    update.callback_query.edit_message_text(text='Выберите мероприятие:', reply_markup=EVENTS_KEYBOARD)
    return "EVENT"


def donate(update: Update, context: CallbackContext):
    update.callback_query.answer()
    update.callback_query.edit_message_text(text='Введите сумму доната', reply_markup=BACK_TO_MENU_KEYBOARD)
    return "START"
