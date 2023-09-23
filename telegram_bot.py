from aiogram.utils import executor
from create_bot import dp
from handlers import client, other, admin
from data_base import sqlite_db


async def strat_up(_):
    print('Бот вышел в онлайн')
    sqlite_db.sql_start()


client.register_handlers_client(dp)
admin.register_handler_admin(dp)
other.register_other_handlers(dp)

executor.start_polling(dp, skip_updates=True, on_startup=strat_up)


# await message.reply(message.text)
# await bot.send_message(message.from_user.id, message.text)
