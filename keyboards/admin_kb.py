from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Admin menu
item1 = KeyboardButton("/upload")
item2 = KeyboardButton("/delete")

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)

kb_admin.add(item1, item2)
