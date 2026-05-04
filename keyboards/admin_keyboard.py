from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.user_keyboard import BACK


def get_main_admin_keyboard():
    keyboard = [
        [InlineKeyboardButton(text='Показать все записи📜', callback_data='all_notes')],
        BACK,
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)