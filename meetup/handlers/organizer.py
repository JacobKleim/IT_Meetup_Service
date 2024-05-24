import requests

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from meetup.keyboards import BACK_TO_MENU_KEYBOARD


def create_event(update: Update, context: CallbackContext) -> None:
    update.callback_query.answer()
    update.callback_query.edit_message_text(text='Введите название мероприятия:')
    return 'GET_EVENT_TITLE'


def get_event_title(update: Update, context: CallbackContext) -> None:
    context.chat_data['event_info'] = {'title': update.message.text}
    update.message.reply_text('Введите описание мероприятия:')
    return 'GET_EVENT_DESCRIPTION'


def get_event_description(update: Update, context: CallbackContext) -> None:
    context.chat_data['event_info']['description'] = update.message.text
    update.message.reply_text('Введите программу мероприятия')
    return 'GET_EVENT_PROGRAM'


def get_event_program(update: Update, context: CallbackContext) -> None:
    context.chat_data['event_info']['event_program'] = update.message.text
    event_data = context.chat_data['event_info']
    title = event_data['title']

    response = requests.post('http://127.0.0.1:8000/api/events/', json=event_data)

    if response.status_code == 201:
        update.message.reply_text(f'Мероприятие {title} создано!', reply_markup=BACK_TO_MENU_KEYBOARD)
    else:
        error_message = response.json()
        update.message.reply_text(f'Произошла ошибка при создании мероприятия: {error_message}', reply_markup=BACK_TO_MENU_KEYBOARD)
    return 'START'
