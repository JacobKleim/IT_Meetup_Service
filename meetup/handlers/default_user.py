import random
import re

from telegram import Update, update
from telegram.ext import CallbackContext, ConversationHandler

from meetup.helpers import get_user_profile
from meetup.keyboards import (
    BACK_TO_MENU_KEYBOARD,
    EVENT_KEYBOARD,
    build_events_keyboard,
    build_speakers_keyboard
)
from meetup.models import UserProfile, Event, Question


def want_meet(update: Update, context: CallbackContext):
    if update.message:
        # обычное сообщение
        current_update = update
        user_reply = update.message.text
        user_id = update.message.from_user.id
    elif update.callback_query:
        # callback
        current_update = update.callback_query
        user_reply = update.callback_query.data
        user_id = update.callback_query.from_user.id
        update.callback_query.answer()
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Что-то пошло не так, обратитесь к администратору",
                                 reply_markup=BACK_TO_MENU_KEYBOARD)
        return "START"

    user_profile, created = UserProfile.objects.get_or_create(telegram_id=user_id)

    if not user_profile.name:
        current_update.message.reply_text("Как к вам обращаться:")
        return "MEETING_NAME"
    elif not user_profile.bio:
        current_update.message.reply_text("Расскажите о себе:")
        return "MEETING_BIO"
    elif not user_profile.contact_info:
        current_update.message.reply_text("Укажите ваши контактные данные:")
        return "MEETING_CONTACT"
    else:
        profiles = UserProfile.objects.exclude(telegram_id=user_id).filter(name__isnull=False, bio__isnull=False,
                                                                           contact_info__isnull=False)
        if profiles.exists():
            random_profile = random.choice(profiles)
            current_update.message.reply_text(
                f"Посмотрите, кого мы вам подобрали\nИмя: {random_profile.name}\nО себе: {random_profile.bio}\nКонтактные данные: {random_profile.contact_info}",
                reply_markup=BACK_TO_MENU_KEYBOARD)
        else:
            current_update.message.reply_text("Пока нет доступных профилей.", reply_markup=BACK_TO_MENU_KEYBOARD)
    return "START"


def ask_name(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_profile = get_user_profile(user_id)
    if not user_profile:
        update.message.reply_text(
            "Не могу найти профиль, обратитесь к администратору",
            reply_markup=BACK_TO_MENU_KEYBOARD
        )
        return "START"

    user_profile.name = update.message.text
    user_profile.save()
    update.message.reply_text("О себе:")
    return "MEETING_BIO"


def ask_bio(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_profile = get_user_profile(user_id)
    if not user_profile:
        update.message.reply_text(
            "Не могу найти профиль, обратитесь к администратору",
            reply_markup=BACK_TO_MENU_KEYBOARD
        )
        return "START"
    user_profile.bio = update.message.text
    user_profile.save()
    update.message.reply_text("Контактные данные:")
    return "MEETING_CONTACT"


def ask_contact_info(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_profile = get_user_profile(user_id)
    if not user_profile:
        update.message.reply_text(
            "Не могу найти профиль, обратитесь к администратору",
            reply_markup=BACK_TO_MENU_KEYBOARD
        )
        return "START"
    user_profile.contact_info = update.message.text
    user_profile.save()
    update.message.reply_text("Спасибо за заполнение анкеты!")
    return want_meet(update, context)


def event_info(update: Update, context: CallbackContext):
    query_data = update.callback_query.data
    update.callback_query.answer()
    event = None
    if re.match(r"^event\d+$", query_data):
        event_id = query_data.replace('event', '')
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            pass
    elif re.match(r"^next_event_info$", query_data):
        event = Event.objects.last()

    if event:
        event_speakers = ', '.join([speaker.name for speaker in event.speakers.all()])
        event_details = (
            f"Название мероприятия: {event.title}\n"
            f"Описание: {event.description}\n"
            f"Программа мероприятия: {event.event_program}\n"
            f"Спикеры: {event_speakers}"
        )
        update.callback_query.edit_message_text(text=event_details, reply_markup=EVENT_KEYBOARD)
        context.chat_data["event"] = event
    else:
        update.callback_query.edit_message_text(
            text="Неправильный выбор или событие не найдено.",
            reply_markup=BACK_TO_MENU_KEYBOARD
        )
    return "EVENT"


def event_schedule(update: Update, context: CallbackContext):
    update.callback_query.answer()
    update.callback_query.edit_message_text(text='Выберите мероприятие:', reply_markup=build_events_keyboard())
    return "EVENT"


def donate(update: Update, context: CallbackContext):
    update.callback_query.answer()
    update.callback_query.edit_message_text(text='Введите сумму доната', reply_markup=BACK_TO_MENU_KEYBOARD)
    return "START"


def contact_speaker(update: Update, context: CallbackContext):
    update.callback_query.answer()
    if context.chat_data["event"]:
        update.callback_query.edit_message_text(
            text='Выберите спикера',
            reply_markup=build_speakers_keyboard(context.chat_data["event"])
        )
        return "ASK_QUESTION"
    else:
        update.callback_query.edit_message_text(
            text='Не могу найти событие, попробуйте снова или обратитесь к администратору',
            reply_markup=BACK_TO_MENU_KEYBOARD
        )
        return "START"


def event_program(update: Update, context: CallbackContext):
    event = context.chat_data.get('event')
    if not event:
        update.callback_query.answer()
        update.callback_query.edit_message_text(
            text='Не могу найти событие, попробуйте снова или обратитесь к администратору',
            reply_markup=BACK_TO_MENU_KEYBOARD
        )
        return 'START'
    reports = event.reports.all().order_by('start_time')
    event_program_text = '\n'.join(
        [f'{talk.subject} - {talk.speaker} - '
         f'{talk.start_time.strftime("%Y-%m-%d %H:%M")} - '
         f'{talk.end_time.strftime("%Y-%m-%d %H:%M")}' for talk in reports])
    event_details = (
        f'Программа мероприятия:\n{event_program_text}'
    )

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=event_details, reply_markup=EVENT_KEYBOARD)

    return 'START'


def ask_question(update: Update, context: CallbackContext):
    query_data = update.callback_query.data
    update.callback_query.answer()
    speaker_id = query_data.replace('speaker', '')
    try:
        speaker = UserProfile.objects.get(pk=speaker_id)
    except UserProfile.DoesNotExist:
        update.message.reply_text("Спикер не найден", reply_markup=BACK_TO_MENU_KEYBOARD)
        return "START"

    context.user_data['speaker_id'] = speaker_id

    update.callback_query.message.reply_text(
        "Пожалуйста, введите ваш вопрос:"
    )
    return "ASK_QUESTION"


def save_question(update: Update, context: CallbackContext):
    # Получить пользователя, задающего вопрос, и текст вопроса
    user_id = update.message.from_user.id
    text = update.message.text

    user_profile = get_user_profile(user_id)
    if not user_profile:
        update.message.reply_text(
            "Не могу найти профиль, обратитесь к администратору",
            reply_markup=BACK_TO_MENU_KEYBOARD
        )
        return ConversationHandler.END

    # Получение спикера из данных контекста
    speaker_id = context.user_data.get('speaker_id')
    if not speaker_id:
        update.message.reply_text("Ошибка внутреннего состояния", reply_markup=BACK_TO_MENU_KEYBOARD)
        return ConversationHandler.END

    try:
        speaker = UserProfile.objects.get(pk=speaker_id)
    except UserProfile.DoesNotExist:
        update.message.reply_text("Спикер не найден", reply_markup=BACK_TO_MENU_KEYBOARD)
        return ConversationHandler.END

    # Сохранение вопроса в базу данных
    question = Question(
        user=user_profile,
        speaker=speaker,
        text=text,
        event=context.chat_data["event"]
    )
    question.save()
    update.message.reply_text("Cпасибо за ваш вопрос!\nВаш вопрос был отправлен спикеру!", reply_markup=BACK_TO_MENU_KEYBOARD)

    # Очистка данных контекста
    context.user_data.pop('speaker_id', None)
    context.chat_data.pop('event', None)

    return "START"