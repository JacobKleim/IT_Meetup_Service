from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_start_keyboard(update, context):
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


EVENTS_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('1 мероприятие', callback_data='event1'),
            InlineKeyboardButton('2 мероприятие', callback_data='event2')
        ],
        [InlineKeyboardButton('В главное меню', callback_data='main_menu')]
    ]
)
EVENT_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Программа мероприятия', callback_data='event_program'),
            InlineKeyboardButton('Задонатить', callback_data='donate'),
            InlineKeyboardButton('Связаться с докладчиком', callback_data='contact_speaker')
        ],
        [InlineKeyboardButton('В главное меню', callback_data='main_menu')]
    ]
)

SPEAKERS_EVENT_KEYBOARD = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton('Докладчик 1', callback_data='speaker1')],
        [InlineKeyboardButton('Докладчик 2', callback_data='speaker2')],
        [InlineKeyboardButton('Докладчик 3', callback_data='speaker3')],
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