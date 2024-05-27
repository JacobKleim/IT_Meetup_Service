from telegram import Update

from meetup.helpers import check_bot_context
from meetup.keyboards import build_start_keyboard


def handle_start(update: Update, context):
    check_bot_context(update, context, force_update=True)
    start_keyboard = build_start_keyboard(update, context)
    update.message.reply_text('Выберите пункт меню:', reply_markup=start_keyboard)
    return "START"


def handle_menu(update: Update, context):
    check_bot_context(update, context, force_update=True)
    start_keyboard = build_start_keyboard(update, context)
    update.callback_query.edit_message_text(
        text='Выберите пункт меню:',
        reply_markup=start_keyboard
    )
    return "START"










