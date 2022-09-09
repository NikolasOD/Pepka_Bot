from aiogram import types, Dispatcher
import string
import json


# @dp.message_handler()
async def censorship_checker(message: types.Message):
	if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
			.intersection(set(json.load(open('cenz.json')))) != set():
		await message.reply('Пепочка не любит маты 😢')
		await message.delete()


def register_other_handlers(dp: Dispatcher):
	dp.register_message_handler(censorship_checker)
