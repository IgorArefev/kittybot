import logging
import os
import sys

import requests
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

load_dotenv()
auth_token = os.getenv('TOKEN')
URL = 'https://api.thecatapi.com/v1/images/search'

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logger.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def get_new_image():
    try:
        response = requests.get(URL)
    except Exception:
        logger.error('Сервер не прислал котика')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())


def wake_up(update, context):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['покажи киску']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=f'Спасибо, что включили меня, {chat.first_name}',
        reply_markup=button
    )
    context.bot.send_photo(chat.id, get_new_image())


def main():
    updater = Updater(token=auth_token)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex(r'покажи киску'),
        new_cat)
    )
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
