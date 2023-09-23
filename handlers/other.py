from aiogram import types, Dispatcher
import json, string
from create_bot import dp, bot
import asyncio
import datetime


@dp.message_handler()
async def echo_send(message: types.message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split()} \
            .intersection(set(json.load(open('cenz.json')))) != set():
        await message.reply('Дурачок ты чё несешь, базар фильтруй')
        await message.delete()
    else:
        await bot.send_message(message.from_user.id, f'Команда не распознана')


# async def check_time():
#    if datetime.datetime.now().second % 3 == 0:
#        await bot.send_message('937385550', f'Данная секунда {datetime.datetime.now().second}')
#    await asyncio.sleep(2)
#    tasks.append(ioloop.create_task(check_time()))


def register_other_handlers(dp: Dispatcher):
    dp.register_message_handler(echo_send)

# ioloop = asyncio.get_event_loop()
# global tasks
# tasks = [ioloop.create_task(check_time())]
# ioloop.run_until_complete(asyncio.wait(tasks))
