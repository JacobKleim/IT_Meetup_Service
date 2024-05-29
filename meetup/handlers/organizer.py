import os
import requests


from django.conf import settings
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from meetup.helpers import get_user_profile
from meetup.models import UserProfile
from meetup.keyboards import BACK_TO_MENU_KEYBOARD


def get_speakers_keyboard():
    speakers = UserProfile.objects.all()
    keyboard = [
        [InlineKeyboardButton(speaker.name, callback_data=f'speaker_{speaker.id}')]
        for speaker in speakers
    ]
    keyboard.append([InlineKeyboardButton("Завершить", callback_data='finalize_event_creation')])
    return InlineKeyboardMarkup(keyboard)


def create_event(update: Update, context: CallbackContext) -> None:
    update.callback_query.answer()
    update.callback_query.edit_message_text(text='Введите название мероприятия:')
    return 'GET_EVENT_TITLE'


def get_event_title(update: Update, context: CallbackContext) -> None:
    context.chat_data['event_info'] = {'title': update.message.text}
    organizer = get_user_profile(update.message.from_user.id).pk
    context.chat_data['event_info']['organizer'] = organizer
    update.message.reply_text('Введите описание мероприятия:')
    return 'GET_EVENT_DESCRIPTION'


def get_event_description(update: Update, context: CallbackContext) -> None:
    context.chat_data['event_info']['description'] = update.message.text
    update.message.reply_text('Введите программу мероприятия')
    return 'GET_EVENT_PROGRAM'


def get_event_program(update: Update, context: CallbackContext) -> None:
    context.chat_data['event_info']['event_program'] = update.message.text
    update.message.reply_text('Выберите спикеров:', reply_markup=get_speakers_keyboard())
    return 'GET_EVENT_SPEAKERS'


def add_speaker(update: Update, context: CallbackContext) -> str:
    query = update.callback_query
    query.answer()

    speaker_id = query.data.split('_')[1]
    if 'speakers' not in context.chat_data['event_info']:
        context.chat_data['event_info']['speakers'] = []
    context.chat_data['event_info']['speakers'].append(speaker_id)

    selected_speakers = context.chat_data['event_info']['speakers']
    selected_speakers_text = ', '.join([
        UserProfile.objects.get(id=speaker_id).name
        for speaker_id in selected_speakers
    ])

    query.edit_message_text(
        text=f'Спикер добавлен. Выбраны спикеры: {selected_speakers_text}. Выберите еще одного или нажмите "Завершить".',
        reply_markup=get_speakers_keyboard()
    )
    return 'GET_EVENT_SPEAKERS'


def finalize_event_creation(update: Update, context: CallbackContext) -> str:
    event_data = context.chat_data['event_info']
    title = event_data['title']
    speakers = event_data.get('speakers', [])
    event_data['speakers'] = [int(speaker_id) for speaker_id in speakers]
    response = requests.post(settings.CREATE_EVENT_URL, json=event_data)

    if response.status_code == 201:
        update.callback_query.edit_message_text(f'Мероприятие "{title}" создано!', reply_markup=BACK_TO_MENU_KEYBOARD)
    else:
        error_message = response.json()
        update.callback_query.edit_message_text(f'Произошла ошибка при создании мероприятия: {error_message}', reply_markup=BACK_TO_MENU_KEYBOARD)
    return 'START'
