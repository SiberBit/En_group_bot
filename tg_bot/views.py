import telebot

from django.shortcuts import render
from En_group_bot.settings import TG_TOKEN, DEBUG, HOST_URL
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from time import sleep

bot = telebot.TeleBot(TG_TOKEN, threaded=False)

if not DEBUG and HOST_URL:
    bot.remove_webhook()
    sleep(1)
    bot.set_webhook(url=f'{HOST_URL}/tg_bot/{TG_TOKEN}')


@csrf_exempt
def webhook(request):
    """Получение webhook'ов"""
    bot.process_new_updates([telebot.types.Update.de_json(request.body.decode("utf-8"))])
    return HttpResponse(status=200)


# ==================== Обработка команд ==================== #

# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text='Привет!\n')
