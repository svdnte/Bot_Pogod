from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import sqlite3

from settings_keyboard import get_settings_keyboard, cancel_keyboard
from exceptions import NoUserDataException

sett_router = Router()


class SettingsStates(StatesGroup):
    choosing_city = State()


@sett_router.message(Command('settings'))
async def settings(message: types.Message):
    try:
        kb = get_settings_keyboard(message.from_user.id)
        await message.answer(text='Параметры:', reply_markup=kb)
    except NoUserDataException:
        await message.answer(text='Произошла ошибка Базы данных.\n'
                                  'Нажмите /start чтобы исправить')


@sett_router.message(SettingsStates.choosing_city)
async def city_chosen(message: types.Message, state: FSMContext):
    con = sqlite3.connect('../db/db.db')
    cur = con.cursor()

    cur.execute(f"""UPDATE user_data SET city = '{message.text}' WHERE user_id = {message.from_user.id}""")
    con.commit()
    await message.answer(text=f'Выбран город {message.text}')

    await state.clear()


@sett_router.callback_query(F.data.startswith('city'))
async def callback_query(callback: types.CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split('&')[1])

    con = sqlite3.connect('../db/db.db')
    cur = con.cursor()

    user_data = cur.execute(f"""SELECT * FROM user_data WHERE user_id = {user_id}""").fetchone()
    con.close()

    if not user_data[2]:
        await state.set_state(SettingsStates.choosing_city)
        await callback.message.edit_text(text='Город не указан. Введите название города или координаты:',
                                         reply_markup=cancel_keyboard())

    else:
        await state.set_state(SettingsStates.choosing_city)
        await callback.message.edit_text(text=f'Указан город {user_data[2]}. Введите новое название города',
                                         reply_markup=cancel_keyboard())


@sett_router.callback_query(F.data == 'cancel')
async def cancel(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()

    try:
        await callback.bot.edit_message_text(text='Параметры:',
                                             reply_markup=get_settings_keyboard(callback.from_user.id),
                                             message_id=callback.message.message_id, chat_id=callback.message.chat.id)
    except NoUserDataException:
        await callback.message.answer(text='Произошла ошибка Базы данных.\n'
                                           'Нажмите /start чтобы исправить')
