import telebot
import os
import json
import requests

import functions.creating_buttons as cb

TOKEN = os.environ.get('TG_TOKEN')
API_URL = 'http://127.0.0.1:8000/api/'
bot = telebot.TeleBot(TOKEN, threaded=False)


# ==================== Обработка команд ==================== #

# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    categories = get_categories()
    bot.send_message(chat_id=chat_id, text='Привет!\n',
                     reply_markup=cb.make_inline_keyboard_categories(categories=categories))


def get_categories(category_id: int = None) -> list:
    api_url = API_URL + 'categories/'
    if category_id == '0':
        category_id = None

    response = requests.get(api_url + f'{category_id}/' if category_id else api_url)

    # если ответ успешен, исключения задействованы не будут
    response.raise_for_status()

    categories = response.json()
    return categories


def get_category_info(category_id: int):
    """Получение информации о категории по id"""
    api_url = API_URL + 'category/'

    response = requests.get(api_url + f'{category_id}/')

    # если ответ успешен, исключения задействованы не будут
    response.raise_for_status()

    category = response.json()
    return category


# ==================== Обработка Inline кнопок ==================== #
@bot.callback_query_handler(func=lambda call: True)
def handle_query(message):
    chat_id = message.message.chat.id
    message_id = message.message.message_id
    data = message.data
    print(data)

    if 'category_id' in data:
        data = json.loads(data)
        category_id = data['category_id']

        # Информация для кнопки назад
        if not category_id == '0':
            try:
                category_info = get_category_info(category_id)
            except Exception as e:
                print(e)
                return

            parent_id = str(category_info['parent_id'])
            category_name = category_info["name"] + '\n'
        else:
            # Кнопка Назад не нужна на 1 уровне дерева
            parent_id = None
            category_name = ''

        try:
            categories = get_categories(category_id=category_id)
        except Exception as e:
            print(e)
            return

        try:
            # Выводим сообщение со списком категорий
            bot.edit_message_text(message_id=message_id, chat_id=chat_id, text=f'{category_name}'
                                                                               f'Выберите категорию',
                                  reply_markup=cb.make_inline_keyboard_categories(categories=categories,
                                                                                  last_category_id=parent_id))
        except Exception as e:
            print(e)
            return


if __name__ == '__main__':
    bot.skip_pending = True
    print('Бот запущен локально...')
    bot.polling()
