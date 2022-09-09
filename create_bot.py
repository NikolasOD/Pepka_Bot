from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from config import telegram_bot_token
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token=telegram_bot_token)
dp = Dispatcher(bot, storage=storage)
