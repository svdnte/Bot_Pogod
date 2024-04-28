from aiogram.utils.keyboard import InlineKeyboardMarkup as markup, InlineKeyboardButton as button
import sqlite3

from exceptions import NoUserDataException


def get_settings_keyboard(user_id):
    con = sqlite3.connect('../db/db.db')
    cur = con.cursor()

    try:
        place = cur.execute(f"""SELECT city FROM user_data WHERE user_id = {user_id}""").fetchone()[0]

        buttons = [
            [button(text=f'Город: {"Не указан" if not place else place[0]}', callback_data=f'city&{user_id}')],
        ]
        keyboard = markup(inline_keyboard=buttons)

        return keyboard

    except TypeError:
        raise NoUserDataException


def empty_keyboard():
    return markup(inline_keyboard=[[]])


def cancel_keyboard():
    return markup(inline_keyboard=[[button(text='Отменить', callback_data='cancel')]])
