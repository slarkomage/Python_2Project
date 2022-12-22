from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b01 = KeyboardButton('Любые')
b02 = KeyboardButton('Умеренно адекватные')
b03 = KeyboardButton('Только адекватные')

start_client = ReplyKeyboardMarkup(resize_keyboard=True)

start_client.add(b01).add(b02).add(b03)


b1 = KeyboardButton('Поиск по ключевым словам')
b2 = KeyboardButton('Популярные GIF')
b3 = KeyboardButton('Случайная GIF')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b1).add(b2).insert(b3)


s1 = KeyboardButton('Найти еще GIF')
s2 = KeyboardButton('Вернуться в меню')

search_client = ReplyKeyboardMarkup(resize_keyboard=True)

search_client.add(s1).add(s2)
