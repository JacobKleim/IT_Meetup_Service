import logging
import os

from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (CallbackQueryHandler, Filters, MessageHandler, ConversationHandler,
                          Updater, CommandHandler)

import meetup.handlers.speaker as speaker_handlers
import meetup.handlers.start as start_handlers
import meetup.handlers.default_user as user_handlers
import meetup.handlers.organizer as org_handlers

load_dotenv()


class Command(BaseCommand):
    help = 'Starts the Telegram bot'

    def handle(self, *args, **options):
        main()


def cancel(update: Update, context):
    update.message.reply_text('Диалог завершен.')
    return ConversationHandler.END


def main():
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    updater = Updater(bot_token)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_handlers.handle_start)],
        states={
            'START': [
                CallbackQueryHandler(start_handlers.handle_menu, pattern='^main_menu$'),

                CallbackQueryHandler(user_handlers.want_meet, pattern='^want_meet$'),
                CallbackQueryHandler(user_handlers.event_info, pattern='^next_event_info$'),
                CallbackQueryHandler(user_handlers.event_schedule, pattern='^event_schedule$'),
                CallbackQueryHandler(org_handlers.create_event, pattern='^create_event$'),
                CallbackQueryHandler(speaker_handlers.answer_questions, pattern='^answer_questions$'),
                ],
            'MEETING_NAME': [
                MessageHandler(Filters.text & ~Filters.command, user_handlers.ask_name)
            ],
            'MEETING_BIO': [
                MessageHandler(Filters.text & ~Filters.command, user_handlers.ask_bio)
            ],
            'MEETING_CONTACT': [
                MessageHandler(Filters.text & ~Filters.command, user_handlers.ask_contact_info)
            ],

            'GET_EVENT_TITLE': [
                MessageHandler(Filters.text & ~Filters.command, org_handlers.get_event_title)
            ],
            'GET_EVENT_DESCRIPTION': [
                MessageHandler(Filters.text & ~Filters.command, org_handlers.get_event_description)
            ],
            'GET_EVENT_PROGRAM': [
                MessageHandler(Filters.text & ~Filters.command, org_handlers.get_event_program),
            ],
            'GET_EVENT_SPEAKERS': [
                CallbackQueryHandler(org_handlers.add_speaker, pattern=r'^speaker_\d+$'),
                CallbackQueryHandler(org_handlers.finalize_event_creation, pattern='^finalize_event_creation$')
            ],
            "QUESTIONS": [
                CallbackQueryHandler(start_handlers.handle_menu, pattern='^main_menu$'),

                CallbackQueryHandler(speaker_handlers.get_question, pattern=r'^question_\d+$'),
                MessageHandler(Filters.text & ~Filters.command, speaker_handlers.get_answer),

            ],
            "ASK_QUESTION": [
                CallbackQueryHandler(start_handlers.handle_menu, pattern='^main_menu$'),

                CallbackQueryHandler(user_handlers.ask_question, pattern=r'^speaker\d+$'),
                MessageHandler(Filters.text & ~Filters.command, user_handlers.save_question),

            ],
            "EVENT": [
                CallbackQueryHandler(start_handlers.handle_menu, pattern='^main_menu$'),
                CallbackQueryHandler(user_handlers.event_info, pattern=r'^event\d+$'),
                CallbackQueryHandler(user_handlers.donate, pattern='^donate$'),
                CallbackQueryHandler(user_handlers.contact_speaker, pattern='^contact_speaker$'),
                CallbackQueryHandler(user_handlers.event_program, pattern='^event_program'),


            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    logger.info('Bot started')

    updater.idle()