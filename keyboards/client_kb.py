from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/prikol')
b2 = KeyboardButton('/riddle')
b3 = KeyboardButton('/products')
b4 = KeyboardButton('/share_number', request_contact=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

kb_client.add(b1).insert(b2).add(b3)
