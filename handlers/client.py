from aiogram import types, Dispatcher

from create_bot import bot, dp

from keyboards import kb_client
from data_base import sqlite_db


@dp.message_handler(commands=['start', 'help'])
async def basic_commands(message: types.message):
    try:
        await bot.send_message(message.from_user.id, 'Приветствую, я тестовый бот', reply_markup=kb_client)
    except:
        await message.reply('Общение только в ЛС')


@dp.message_handler(commands=['prikol'])
async def prikol_command(message: types.message):
    await bot.send_message(message.from_user.id, 'Щас будет прикол')


@dp.message_handler(commands=['riddle'])
async def riddle_command(message: types.message):
    await bot.send_message(message.from_user.id, 'Щас будет загадка')


@dp.message_handler(commands=['products'])
async def veiw_products(message: types.Message):
    await sqlite_db.sql_read(message)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(basic_commands, commands=['start', 'help'])
    dp.register_message_handler(prikol_command, commands=['prikol'])
    dp.register_message_handler(riddle_command, commands=['riddle'])
    dp.register_message_handler(veiw_products, commands=['products'])
