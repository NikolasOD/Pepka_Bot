import requests
import random
from datetime import datetime
from aiogram import types, Dispatcher
from config import open_weather_token
from create_bot import bot, dp
from keyboards import kb_client
from data_base import sqlite_db
from aiogram.dispatcher.filters import Text


# WELCOME MESSAGE + START MENU
# @dp.message_handler(commands=['start', 'help'])
async def start_command(message: types.Message):
    sti = open('welcome.webp', 'rb')
    await bot.send_sticker(message.chat.id, sti)
    b_n = await bot.get_me()
    u_n = message.from_user
    await bot.send_message(message.chat.id, """Добро пожаловать, {0.first_name}!
Я - <b>{1.first_name}</b>, бот созданный чтобы помогать.""".format(u_n, b_n), parse_mode='html', reply_markup=kb_client)


# RANDOM NUMBER
async def random_number(message: types.Message):
    await bot.send_message(message.chat.id, f"🎲 Random number: {str(random.randint(0, 100))}")


# HOW ARE YOU
async def how_are_you(message: types.Message):
    hay_markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Fine", callback_data='im_good')
    item2 = types.InlineKeyboardButton("Bad", callback_data='im_bad')
    hay_markup.add(item1, item2)
    await bot.send_message(message.chat.id, 'I\'m fine, how are you?', reply_markup=hay_markup)


@dp.callback_query_handler(Text(startswith='im_'))
async def how_are_you_call(callback: types.CallbackQuery):
    joke_markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Yah, I want", callback_data='im_joke'))
    if str(callback.data.split('_')[1]) == 'good':
        await callback.message.answer('I\'m glad for you 😊')
    elif str(callback.data.split('_')[1]) == 'bad':
        await callback.message.answer('Oh this is so sad, want a joke? 😊', reply_markup=joke_markup)
    elif str(callback.data.split('_')[1]) == 'joke':
        jokes = ['В Росії дві біди - дураки і дороги. А в Україні три - дураки, дороги та Росія',
                 'Смс спілкування - ти шо робиш ?- засипаю.Без мене засинаєш?-москаля землею засипаю!',
                 'У конкурсі “Україна очима москалів” переміг пан Василь зі Львова, який виклав очима москалів '
                 'триметрове слово “Україна”']
        await callback.message.answer(random.choice(jokes))

# @dp.message_handler(content_types=['text'])
# def lalala(message):
# 	if message.chat.type == 'private':
# 		if message.text == "🌤️ Погода":
# 			markup = types.ForceReply(selective=False)
# 			bot.send_message(message.chat.id, "Введите город или страну:", reply_markup=markup)
# 		elif message.text == '😊 Как дела?':
#
# 			markup = types.InlineKeyboardMarkup(row_width=2)
# 			item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
# 			item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')
#
# 			markup.add(item1, item2)
#
# 			bot.send_message(message.chat.id, 'Отлично, сам как?', reply_markup=markup)
# 		else:
# 			bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')


# WEATHER
# @dp.message_handler(commands=['weather'])
async def get_weather(message: types.Message):
    await message.reply("Input city")
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        city = data["name"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.fromtimestamp(data["sys"]["sunset"])
        await message.answer(f"Погода в городе {city}:\nТемпература: {temp}C°\n"
                             f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст.\nВетер: {wind} м/с\n"
                             f"Восход солнца: {sunrise_timestamp}\n"
                             f"Закат солнца: {sunset_timestamp}\n"
                             f"Хорошего дня!"
                             )
    except:
        await message.reply("Проверьте название города")


# CRYPTOCURRENCY
async def get_data(message: types.Message):
    req = requests.get("https://yobit.net/api/3/ticker/btc_usd")
    response = req.json()
    sell_price = response["btc_usd"]["sell"]
    # return f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nSell BTC price: {sell_price}"
    await bot.send_message(message.chat.id,
                           f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nSell BTC price: {sell_price}")


async def storage_menu_command(message: types.Message):
    await sqlite_db.sql_read(message)


# Register handlers
def register_client_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start', 'help'])
    # dp.register_message_handler(get_weather, commands='weather')
    dp.register_message_handler(get_data, commands='crypto')
    dp.register_message_handler(random_number, commands='random_number')
    dp.register_message_handler(how_are_you, commands="how_are_you")
    dp.register_message_handler(storage_menu_command, commands="storage")
    # dp.register_callback_query_handler(how_are_you_call, text=['good', 'bad'])
