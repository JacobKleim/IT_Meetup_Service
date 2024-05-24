from telegram import Update, InlineKeyboardButton
from telegram.ext import CallbackContext, ConversationHandler

from meetup.helpers import check_bot_context
from meetup.keyboards import EVENTS_KEYBOARD, EVENT_KEYBOARD, get_start_keyboard, BACK_TO_MENU_KEYBOARD


# def handle_start(update: Update, context: CallbackContext) -> str:
#     update.message.reply_text('Привет, я бот IT MEETUP')
#     show_menu(update, context)
#     return 'CHOOSING'
#
#
# def handle_welcome_choice(update: Update, context:CallbackContext):
#     query = update.callback_query
#     if not query:
#         return 'CHOOSING'
#     callback = query.data
#     if callback == 'event_schedule':
#         query.message.reply_text('Тут будет список мероприятий', reply_markup=EVENTS_KEYBOARD)
#         context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
#         return 'HANDLE_EVENT'
#     elif callback == 'next_event_info':
#         query.message.reply_text('Информация о мероприятии x', reply_markup=EVENT_KEYBOARD)
#         context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
#         return 'HANDLE_EVENT'
#
#
# def show_menu(update: Update, context: CallbackContext):
#     keyboard = START_KEYBOARD
#     if context.user_data['user'].is_organizer:
#         keyboard.inline_keyboard.append([InlineKeyboardButton('Создать мероприятие', callback_data='create_event')])
#     if context.user_data['user'].is_speaker:
#         keyboard.inline_keyboard.append([InlineKeyboardButton('Ответить на вопросы', callback_data='answer_questions')])
#
#     context.bot.send_message(
#         chat_id=update.effective_chat.id,
#         text='Выберите пункт меню',
#         reply_markup=keyboard
#     )
#     context.bot.delete_message(
#         chat_id=update.effective_chat.id,
#         message_id=update.effective_message.message_id
#    )
def handle_start(update: Update, context):
    check_bot_context(update, context)
    start_keyboard = get_start_keyboard(update, context)
    update.message.reply_text('Выберите пункт меню:', reply_markup=start_keyboard)
    return "START"


def handle_menu(update: Update, context):
    start_keyboard = get_start_keyboard(update, context)
    update.callback_query.edit_message_text(
        text='Выберите пункт меню:',
        reply_markup=start_keyboard
    )
    return "START"










