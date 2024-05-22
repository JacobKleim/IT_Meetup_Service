import logging
import os
import requests

from meetup.models import *
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardMarkup)
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler,
                          Updater)
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
load_dotenv()


class Command(BaseCommand):
    help = 'Starts the Telegram bot'

    def handle(self, *args, **options):
        bot_token = os.environ['TELEGRAM_BOT_TOKEN']
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.DEBUG)
        logger = logging.getLogger(__name__)
        logger.info('Bot started')

        def start(update: Update, context: CallbackContext) -> None:
            update.message.reply_text('Привет, я бот IT MEETUP')
            keyboard = [
                        [InlineKeyboardButton(
                            'Создать мероприятие', callback_data='Создать мероприятие')],
                        [InlineKeyboardButton(
                            'Хочу познакомиться', callback_data='Создать мероприятие')],
                        [InlineKeyboardButton(
                            'Информация о мероприятии', callback_data='Информация о мероприятии')], 
                        [InlineKeyboardButton(
                            'Узнать расписание мероприятия', callback_data='Узнать расписание мероприятия')],    

                    ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(
                        'Вот что я умею',
                        reply_markup=reply_markup)

        updater = Updater(bot_token)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler('start', start))

        updater.start_polling()
        updater.idle()