from telebot import types


def make_inline_keyboard_categories(categories: list, last_category_id: int = None) -> types.InlineKeyboardMarkup:
    """Создаём кнопки c категориями"""
    markup = types.InlineKeyboardMarkup()
    for category in categories:
        name = category['name']
        category_id = str(category['id'])
        parent_id = str(category['parent_id'])
        data = '{"category_id": "' + category_id + '","parent_id":"' + parent_id +'"}'
        markup.add(types.InlineKeyboardButton(text=name, callback_data=data))

    if last_category_id:
        # id предыдущей категории
        data = '{"category_id": "' + last_category_id + '","parent_id":"' + last_category_id + '"}'
        markup.add(types.InlineKeyboardButton(text='<', callback_data=data))

    return markup
