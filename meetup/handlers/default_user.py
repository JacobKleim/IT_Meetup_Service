import random
import re

from telegram import Update
from telegram.ext import CallbackContext

from meetup.helpers import get_user_profile
from meetup.keyboards import (
    BACK_TO_MENU_KEYBOARD,
    SPEAKERS_EVENT_KEYBOARD,
    EVENT_KEYBOARD, EVENTS_KEYBOARD
)
from meetup.models import UserProfile


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
                                 text="Что-то пошло не так, возвращаю в начало")
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
