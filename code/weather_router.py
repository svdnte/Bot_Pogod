from aiogram import Router, F, Bot
from aiogram.filters.command import Command, CommandObject
from aiogram import types

import requests
import sqlite3

from to_normal_format import *
from weather_keyboard import get_weather_keyboard, get_back_keyboard

API_KEY = "01273c8446754262b4e83400241603"

address_forecast = "http://api.weatherapi.com/v1/forecast.json"
address_current = "http://api.weatherapi.com/v1/current.json"

weather_router = Router()


@weather_router.message(Command('weather'))
async def weather(message: types.Message, command: CommandObject):
    con = sqlite3.connect('../db/db.db')
    cur = con.cursor()

    try:
        user_city = cur.execute(f"""SELECT city FROM user_data WHERE user_id = {message.from_user.id}""").fetchone()[0]

        if user_city and command.args is None:
            await message.answer(text='Выберите нужный вариант:',
                                 reply_markup=get_weather_keyboard(message.from_user.id,
                                                                   user_city))
        else:
            if not command.args:
                await message.answer(text='Не указан аргумент: Город или координаты.\n'
                                          'Вы также можете привязать город - /settings')
            else:
                await message.answer(text='Выберите нужный вариант:',
                                     reply_markup=get_weather_keyboard(message.from_user.id,
                                                                       command.args))

    except TypeError:
        await message.answer(text='Произошла ошибка Базы данных.\n'
                                  'Нажмите /start чтобы исправить')


@weather_router.callback_query(F.data.startswith('weather_now'))
async def weather_now(callback: types.CallbackQuery):
    callback_name, user_id, place = callback.data.split('&')

    data = requests.get(address_current,
                        params={'key': API_KEY, 'q': place, 'aqi': 'yes', 'lang': 'ru', 'alerts': 'yes'}).json()

    text = to_current(data)

    await callback.message.edit_text(text, reply_markup=get_back_keyboard(place))


@weather_router.callback_query(F.data.startswith('back'))
async def back(callback: types.CallbackQuery):
    await callback.bot.edit_message_text(text='Выберите нужный вариант:',
                                         reply_markup=get_weather_keyboard(callback.message.from_user.id,
                                                                           callback.data.split('&')[1]),
                                         message_id=callback.message.message_id, chat_id=callback.message.chat.id)


@weather_router.callback_query(F.data.startswith('forecast_today'))
async def forecast_today(callback: types.CallbackQuery):
    callback_name, user_id, place = callback.data.split('&')
    data = requests.get(address_forecast,
                        params={'key': API_KEY, 'q': place, 'aqi': 'yes', 'lang':
                            'ru', 'alerts': 'yes', 'days': 1}).json()

    text = to_today_forecast(data)

    await callback.message.edit_text(text=text, reply_markup=get_back_keyboard(place))


@weather_router.callback_query(F.data.startswith('forecast_zavtra'))
async def forecast_tomorrow(callback: types.CallbackQuery):
    callback_name, user_id, place = callback.data.split('&')
    data = requests.get(address_forecast,
                        params={'key': API_KEY, 'q': place, 'aqi': 'yes', 'lang':
                            'ru', 'alerts': 'yes', 'days': 2}).json()

    text = to_tomorrow_forecast(data)

    await callback.message.edit_text(text=text, reply_markup=get_back_keyboard(place))


@weather_router.callback_query(F.data.startswith('forecast_poslezavtra'))
async def forecast_tomorrow_tomorrow(callback: types.CallbackQuery):
    callback_name, user_id, place = callback.data.split('&')
    data = requests.get(address_forecast,
                        params={'key': API_KEY, 'q': place, 'aqi': 'yes', 'lang':
                            'ru', 'alerts': 'yes', 'days': 3}).json()

    text = to_tomorrow_tomorrow_forecast(data)

    await callback.message.edit_text(text=text, reply_markup=get_back_keyboard(place))
