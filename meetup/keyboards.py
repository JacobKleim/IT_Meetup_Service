from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from meetup.models import Event


def build_start_keyboard(update, context):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton('Хочу познакомиться', callback_data='want_meet')],
            [InlineKeyboardButton('Информация о ближайшем мероприятии', callback_data='next_event_info')],
            [InlineKeyboardButton('Узнать расписание мероприятия', callback_data='event_schedule')],
        ]
    )
    if context.user_data.get('user', {}).is_organizer:
        keyboard.inline_keyboard.append([InlineKeyboardButton('Создать мероприятие', callback_data='create_event')])
    if context.user_data.get('user', {}).is_speaker:
        keyboard.inline_keyboard.append([InlineKeyboardButton('Ответить на вопросы', callback_data='answer_questions')])
    return keyboard


def build_events_keyboard():
    events = Event.objects.all()
    keyboard = []
    if not events.exists():
        keyboard.append([InlineKeyboardButton('Нет мероприятий:(', callback_data='main_menu')])
    else:
        for event in events:
            keyboard.append([InlineKeyboardButton(f"{event.id}. {event.title}", callback_data=f"event{event.id}")])
    keyboard.append([InlineKeyboardButton('В главное меню', callback_data='main_menu')])
    return InlineKeyboardMarkup(keyboard)


def build_speakers_keyboard(event):
    speakers = event.speakers.all()
    keyboard = []
    if not speakers.exists():
        keyboard.append([InlineKeyboardButton('Нет спикеров:(', callback_data='main_menu')])
    else:
        for speaker in speakers:
            name = speaker.name if speaker.name else speaker.telegram_id
            keyboard.append([InlineKeyboardButton(
                f"Спикер {name}", callback_data=f"speaker{speaker.id}")])
    keyboard.append([InlineKeyboardButton('В главное меню', callback_data='main_menu')])
    return InlineKeyboardMarkup(keyboard)


EVENT_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Программа мероприятия', callback_data='event_program'),
            InlineKeyboardButton('Задонатить', callback_data='donate'),
            InlineKeyboardButton('Связаться со спикером', callback_data='contact_speaker')
        ],
        [InlineKeyboardButton('В главное меню', callback_data='main_menu')]
    ]
)


BACK_TO_MENU_KEYBOARD = InlineKeyboardMarkup(
    [[InlineKeyboardButton('В главное меню', callback_data='main_menu')]]
)
QUESTIONS_KEYBOARD = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton('Вопрос 1', callback_data='question_1')],
        [InlineKeyboardButton('Вопрос 2', callback_data='question_2')],
        [InlineKeyboardButton('В главное меню', callback_data='main_menu')]
    ]
)