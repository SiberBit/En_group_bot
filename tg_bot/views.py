from django.shortcuts import render
from En_group_bot.settings import TG_TOKEN

import telebot


bot = telebot.TeleBot(TG_TOKEN, threaded=False)


# ==================== Обработка команд ==================== #

# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text='Привет!\n')
