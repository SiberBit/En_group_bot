import telebot
import os
import json

import functions.creating_buttons as cb
from functions.api import API

TOKEN = os.environ.get('TG_TOKEN')
API_TOKEN = os.environ.get('API_TOKEN')

API_URL = os.environ.get('API_URL')
ORGANIZATION_SLUG = os.environ.get('ORGANIZATION_SLUG')
DEPARTAMENT_SLUG = os.environ.get('DEPARTAMENT_SLUG')

if not (API_URL and ORGANIZATION_SLUG and DEPARTAMENT_SLUG):
    API_URL = 'http://127.0.0.1:8000/api/v1/'
    ORGANIZATION_SLUG = 'testovaya-organizaciya'
    DEPARTAMENT_SLUG = 'podrazdelenie-1'

bot = telebot.TeleBot(TOKEN, threaded=False)

api = API(api_url=API_URL, organization_slug=ORGANIZATION_SLUG, department_slug=DEPARTAMENT_SLUG, token=API_TOKEN)


# ==================== Обработка команд ==================== #

# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    categories = api.get_categories()
    bot.send_message(chat_id=chat_id, text='''Привет! Я Ваш личный бот помощник🦾\n
                                            Выбирайте категории вопросов, которые Вас интересуют,\n
                                            там Вы найдете ответы на большинство вопросов по выбранной теме🥳\n 
                                            Если Вы не нашли интересующий Вас вопрос😰, свяжитесь с Call-центром🙄
                                                                                '''
                                           ,
                     reply_markup=cb.make_inline_keyboard_categories(categories=categories))


# Команда /help
@bot.message_handler(commands=['help'])
def start_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text='''Привет! Я Ваш личный бот помощник🦾\n
                                            Выбирайте категории вопросов, которые Вас интересуют,\n
                                            там Вы найдете ответы на большинство вопросов по выбранной теме🥳\n 
                                            Если Вы не нашли интересующий Вас вопрос😰, свяжитесь с Call-центром🙄
                                                                                ''')


# ==================== Обработка Inline кнопок ==================== #
@bot.callback_query_handler(func=lambda call: True)
def handle_query(message):
    chat_id = message.message.chat.id
    message_id = message.message.message_id
    data = message.data
    print('callback data: ', data)

    if 'category_id' in data:
        data = json.loads(data)
        category_id = data['category_id']

        target = data['target']

        # Информация для кнопки назад
        if not category_id == '0':
            try:
                category_info = api.get_category_info(category_id)
            except Exception as e:
                print(e)
                return

            parent_id = str(category_info['parent_id'])
            category_name = category_info["name"] + '\n'
        else:
            # Кнопка Назад не нужна на 1 уровне дерева
            parent_id = None
            category_name = ''

        if target == 'categories':

            try:
                # получаем категории через API
                categories = api.get_categories(category_id=category_id)
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

        elif target == 'questions':

            try:
                # получаем вопросы через API
                questions = api.get_questions(category_id=category_id)
            except Exception as e:
                print(e)
                return
            print(questions)
            try:
                # Выводим сообщение со списком вопросов
                bot.edit_message_text(message_id=message_id, chat_id=chat_id, text=f'{category_name}'
                                                                                   f'Выберите вопрос',
                                      reply_markup=cb.make_inline_keyboard_questions(questions=questions,
                                                                                     last_category_id=parent_id))
            except Exception as e:
                print(e)
                return


    elif 'question_id' in data:
        data = json.loads(data)
        question_id = data['question_id']
        category_id = data['category']

        try:
            question_info = api.get_question_info(question_id=question_id)
        except Exception as e:
            print(e)
            return

        question = question_info['question']
        answer = question_info['answer']

        try:
            # Выводим сообщение со списком вопросов
            bot.edit_message_text(message_id=message_id, chat_id=chat_id, text=f'<b>Вопрос:</b>\n'
                                                                               f'{question}\n\n'
                                                                               f'<b>Ответ:</b>\n'
                                                                               f'{answer}',
                                  reply_markup=cb.make_inline_keyboard_back_from_question(category_id=category_id),
                                  parse_mode='HTML')
        except Exception as e:
            print(e)
            return


if __name__ == '__main__':
    bot.skip_pending = True
    print('Бот запущен локально...')
    bot.polling()
