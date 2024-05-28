from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from meetup.helpers import get_user_profile
from meetup.keyboards import (
    BACK_TO_MENU_KEYBOARD,
    build_questions_keyboard
)
from meetup.models import Question


def answer_questions(update: Update, context: CallbackContext):
    user_id = update.callback_query.from_user.id
    speaker = get_user_profile(user_id)
    update.callback_query.edit_message_text(
        text='Вот вопросы которые подготовили пользователи',
        reply_markup=build_questions_keyboard(speaker))
    return "QUESTIONS"


def get_question(update: Update, context: CallbackContext):
    question_id = update.callback_query.data.replace('question_', '')
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        update.callback_query.edit_message_text(
            'Вопрос не найден',
            reply_markup=BACK_TO_MENU_KEYBOARD
        )
        return ConversationHandler.END

    update.callback_query.edit_message_text(
        text=f'Вопрос № {question_id}. {question.text}\n Введите ваш ответ'
    )
    update.callback_query.answer()
    context.chat_data['question_id'] = question_id
    return "QUESTIONS"


def get_answer(update: Update, context: CallbackContext):
    question_id = context.chat_data.get('question_id')
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        update.callback_query.edit_message_text(
            'Вопрос не найден',
            reply_markup=BACK_TO_MENU_KEYBOARD
        )
        return ConversationHandler.END
    question.answer = update.message.text
    question.save()
    context.bot.send_message(
        chat_id=question.user.telegram_id,
        text=f'Спикер {question.speaker.name} ответил на ваш вопрос!\nВопрос: {question.text}\nОтвет: {question.answer}'
    )

    update.message.reply_text(
        text=f'Ваш ответ на вопрос № {question_id} принят',
        reply_markup=BACK_TO_MENU_KEYBOARD
    )
    return "START"
