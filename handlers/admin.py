from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from data_base import sqlite_db
from keyboards import admin_kb

from create_bot import dp, bot
from create_bot import password


class FSM_admin(StatesGroup):
    password = State()
    photo = State()
    name = State()
    description = State()
    price = State()


@dp.message_handler(commands=['Админ'])
async def admin(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выберите команду', reply_markup=admin_kb.button_case_admin)
    await message.delete()


# начало загрузки меню
@dp.message_handler(commands=['Загрузить'], state=None)
async def cm_start(message: types.Message):
    await message.reply('Введите пароль')
    await FSM_admin.password.set()


@dp.message_handler(state=FSM_admin.password)
async def password_check(message: types.Message, state: FSMContext):
    if str(message.text) == password:
        await message.reply('Пароль верный, загрузите фото')
        await FSM_admin.photo.set()
    else:
        await message.reply('Пароль неверный')
        await state.finish()


# выход из загрузки
@dp.message_handler(state="*", commands=['отмена'])
@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ОК')


# фиксируем первый ответ
@dp.message_handler(content_types=['photo'], state=FSM_admin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSM_admin.next()
    await message.reply('Теперь ведите название')


# второй ответ
@dp.message_handler(state=FSM_admin.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSM_admin.next()
    await message.reply('Введите описание')


@dp.message_handler(state=FSM_admin.description)
async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['descritption'] = message.text
    await FSM_admin.next()
    await message.reply('Введи цену')


@dp.message_handler(state=FSM_admin.price)
async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)

    await sqlite_db.sql_add_command(state)
    await state.finish()


def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSM_admin.photo)
    dp.register_message_handler(load_name, state=FSM_admin.name)
    dp.register_message_handler(load_description, state=FSM_admin.description)
    dp.register_message_handler(load_price, state=FSM_admin.price)
    dp.register_message_handler(cancel_handler, state="*", commands=['отмена'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(admin, commands=['Админ'])
