from telegram import Update
from telegram.ext import CallbackContext

from meetup.keyboards import BACK_TO_MENU_KEYBOARD


def create_event(update: Update, context: CallbackContext):
    update.callback_query.answer()
    update.callback_query.edit_message_text(text='Создание мероприятия.', reply_markup=BACK_TO_MENU_KEYBOARD)
    return "START"
