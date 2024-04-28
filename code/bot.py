import asyncio
import logging
import sqlite3

import aiogram.utils.token
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from settings_router import sett_router
from weather_router import weather_router


with open('../TOKEN.txt', mode='r') as token_file:
    TOKEN = token_file.readline()

logging.basicConfig(level=logging.INFO)

try:
    bot = Bot(token=TOKEN)
    # Username -- @Bot1Pogod_bot
except aiogram.utils.token.TokenValidationError:
    raise aiogram.utils.token.TokenValidationError('Не указан токен или указан несуществующий! Проверьте файл TOKEN.txt')

dp = Dispatcher()
dp.include_routers(sett_router, weather_router)


@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer(text=f'Привет, {message.from_user.first_name}\n\nЭтот бот поможет тебе следить за погодой.\n\n'
                              f'Основные функции:\n'
                              f'/weather   - Меню прогноза погоды для выбранного места\n'
                              f'/settings  - Настройки')

    con = sqlite3.connect('../db/db.db')
    cur = con.cursor()

    try:
        cur.execute(f"""INSERT INTO user_data (user_id) VALUES ({message.from_user.id})""")
        con.commit()
        con.close()

    except sqlite3.IntegrityError:
        logging.log(level=logging.WARNING, msg=f'User (Tg_id={message.from_user.id}) already exists in the database')


@dp.message(Command('help'))
async def help_(message: types.Message):
    await message.answer(text='''Команды:
        
    /weather -- Прогноз погоды для выбранного места
Может использоваться как с аргументом, так и без него (если место указано в настройках)
Примеры использования:
    * /weather Санкт-Петербург (С аргументом)
    * /weather (Без аргумента, будет работать если город или координаты указаны в настройках)
    
    /setting -- Параметры
    
    /help -- Помощь
    
    По вопросам работы бота обращаться: @svdnte''')


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
