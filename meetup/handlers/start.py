from telegram import Update
from telegram.ext import CallbackContext

from meetup.keyboards import START_KEYBOARD


def handle_start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет, я бот IT MEETUP')

    update.message.reply_text(
        'Вот что я умею',
        reply_markup=START_KEYBOARD)
