from telegram import Update
from telegram.ext import CallbackContext

from meetup.keyboards import QUESTIONS_KEYBOARD, BACK_TO_MENU_KEYBOARD


def answer_questions(update: Update, context: CallbackContext):
    update.callback_query.edit_message_text(
        text='Вот вопросы которые подготовили пользователи',
        reply_markup=QUESTIONS_KEYBOARD)
    return "QUESTIONS"


def get_question(update: Update, context: CallbackContext):
    question_id = update.callback_query.data.replace('question_', '')
    update.callback_query.edit_message_text(
        text=f'Вопрос № {question_id}. Текст вопроса\n Введите ваш ответ'
    )
    update.callback_query.answer()
    return "QUESTIONS"


def get_answer(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=f'Ваш ответ на вопрос принят',
        reply_markup=BACK_TO_MENU_KEYBOARD
    )
    return "START"
