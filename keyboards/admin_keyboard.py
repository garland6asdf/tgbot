from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_admin_keyboard():
    keyboard = [
        [InlineKeyboardButton(text='Показать все записи', callback_data='all_notes')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)