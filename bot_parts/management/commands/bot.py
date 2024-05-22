import logging
import os

from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (CallbackQueryHandler, Filters, MessageHandler)
from telegram.ext import Updater, CommandHandler, CallbackContext

import bot_parts.handlers.start as start_handlers

load_dotenv()


class Command(BaseCommand):
    help = 'Starts the Telegram bot'

    def handle(self, *args, **options):
        main()


def user_input_handler(update: Update, context: CallbackContext):
    # получаем тело сообщения
    if update.message:
        # обычное сообщение
        user_reply = update.message.text
    elif update.callback_query.data:
        # callback
        user_reply = update.callback_query.data
    else:
        return

    if user_reply == '/start':
        #TODO заменить на user_data['user'].state как будут модели
        context.user_data['state'] = 'START'
        user_state = 'START'
    else:
        user_state = context.user_data['state'] or 'START'

    # мапа, возвращающая callback функции для вызова дальше.
    states_function = {
        # start
        'START': start_handlers.handle_start,
    }
    # вызываем функцию для получения state
    state_handler = states_function[user_state]
    # получаем некст state
    next_state = state_handler(update, context)
    # записываем следующий state в юзера
    context.user_data['state'] = next_state
    # context.user_data['user'].state = next_state
    # context.user_data['user'].save()


def main():
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    updater = Updater(bot_token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', user_input_handler))
    dp.add_handler(CallbackQueryHandler(user_input_handler))
    dp.add_handler(MessageHandler(Filters.text, user_input_handler))
    updater.start_polling()
    logger.info('Bot started')

    updater.idle()


