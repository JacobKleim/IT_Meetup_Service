from telegram import InlineKeyboardButton, InlineKeyboardMarkup

START_KEYBOARD = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton('Создать мероприятие', callback_data='create_event')],
        [InlineKeyboardButton('Хочу познакомиться', callback_data='want_meet')],
        [InlineKeyboardButton('Информация о мероприятии', callback_data='event_info')],
        [InlineKeyboardButton('Узнать расписание мероприятия', callback_data='event_schedule')],
    ]
)
