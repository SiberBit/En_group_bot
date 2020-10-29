from telebot import types


def make_inline_keyboard_categories(categories: list, last_category_id: int = None) -> types.InlineKeyboardMarkup:
    """Создаём кнопки c категориями"""
    markup = types.InlineKeyboardMarkup()
    for category in categories:
        name = category['name']
        category_id = str(category['id'])
        parent_id = str(category['parent_id'])
        target = category['target']
        data = '{"category_id": "' + category_id + '","parent_id":"' + parent_id + '","target":"' + target + '"}'
        markup.add(types.InlineKeyboardButton(text=name, callback_data=data))

    if last_category_id:
        # id предыдущей категории
        data = '{"category_id": "' + last_category_id + '","parent_id":"' + last_category_id + '","target":"categories"}'
        markup.add(types.InlineKeyboardButton(text='<', callback_data=data))

    return markup


def make_inline_keyboard_questions(questions: list, last_category_id: int = None) -> types.InlineKeyboardMarkup:
    """Создаём кнопки c категориями"""
    markup = types.InlineKeyboardMarkup()
    for question in questions:
        text = question['question']
        question_id = str(question['id'])
        category = str(question['category'])
        data = '{"question_id": "' + question_id + '","category":"' + category + '"}'
        markup.add(types.InlineKeyboardButton(text=text, callback_data=data))

    if last_category_id:
        # id предыдущей категории
        data = '{"category_id": "' + last_category_id + '","parent_id":"' + last_category_id + '","target":"categories"}'
        markup.add(types.InlineKeyboardButton(text='<', callback_data=data))

    return markup


def make_inline_keyboard_back_from_question(category_id: int = None) -> types.InlineKeyboardMarkup:
    """Создаём кнопки c категориями"""
    markup = types.InlineKeyboardMarkup()

    # id категории
    data = '{"category_id": "' + category_id + '","parent_id":"' + category_id + '","target":"questions"}'
    markup.add(types.InlineKeyboardButton(text='<', callback_data=data))

    return markup