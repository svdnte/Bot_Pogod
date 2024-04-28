from aiogram.utils.keyboard import InlineKeyboardMarkup as markup, InlineKeyboardButton as button


def get_weather_keyboard(user_id, address):
    buttons = [
        [button(text='Погода сейчас', callback_data=f'weather_now&{user_id}&{address}')],
        [button(text='Прогноз на сегодня', callback_data=f'forecast_today&{user_id}&{address}')],
        [button(text='Прогноз на завтра', callback_data=f'forecast_zavtra&{user_id}&{address}')],
        [button(text='Прогноз на послезатра', callback_data=f'forecast_poslezavtra&{user_id}&{address}')],
    ]

    keyboard = markup(inline_keyboard=buttons)

    return keyboard


def get_back_keyboard(place):
    keyboard = markup(inline_keyboard=[[button(text='Назад', callback_data=f'back&{place}')]])

    return keyboard


def empty_keyboard():
    return markup(inline_keyboard=[[]])
