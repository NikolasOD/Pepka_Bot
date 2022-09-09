from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Client menu
item1 = KeyboardButton("/random_number")
item2 = KeyboardButton("/how_are_you")
item3 = KeyboardButton("/storage")
item4 = KeyboardButton("/crypto")

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)

kb_client.add(item1, item2, item3, item4)
