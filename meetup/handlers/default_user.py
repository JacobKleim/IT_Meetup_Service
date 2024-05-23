from meetup.keyboards import BACK_TO_MENU_KEYBOARD, SPEAKERS_EVENT_KEYBOARD


def handle_event(update, context):
    query = update.callback_query
    if not query:
        return 'HANDLE_EVENT'
    callback = query.data
    if callback == 'event_program':
        query.message.reply_text(
            'Расписание мероприятия(логично сделать кнопки с временем и проваливаться в доклад)',
            reply_markup=BACK_TO_MENU_KEYBOARD)
        context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        return 'HANDLE_EVENT'
    elif callback == 'donate':
        query.message.reply_text('Введите сумму доната и отправьте ее в никуда', reply_markup=BACK_TO_MENU_KEYBOARD)
        return 'HANDLE_EVENT'
    elif callback == 'contact_speaker':
        query.message.reply_text('Выберите докладчика', reply_markup=SPEAKERS_EVENT_KEYBOARD)
        return 'HANDLE_EVENT'


