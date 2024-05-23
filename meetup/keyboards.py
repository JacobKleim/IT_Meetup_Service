from telegram import InlineKeyboardButton, InlineKeyboardMarkup

START_KEYBOARD = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton('Хочу познакомиться', callback_data='want_meet')],
        [InlineKeyboardButton('Информация о ближайшем мероприятии', callback_data='next_event_info')],
        [InlineKeyboardButton('Узнать расписание мероприятия', callback_data='event_schedule')],
    ]
)

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