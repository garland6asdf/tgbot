from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

BACK_KEYBOARD = [InlineKeyboardButton(text='Вернуться в главное меню', callback_data='back')]
WRITING = [InlineKeyboardButton(text='Продолжить', callback_data='start_writting')]

def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton(text='О боте', callback_data='about')],
        [InlineKeyboardButton(text='Записать свои данные', callback_data='writing_to_db')],
        [InlineKeyboardButton(text='Узнать свой ID', callback_data='user_id')],
        [InlineKeyboardButton(text='Для админов', callback_data='admin_panel')],
        [InlineKeyboardButton(text='Покажите мою инфу', callback_data='info_about_user')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_back_keyboard(writing=False):
    keyboard = [
        BACK_KEYBOARD
    ]
    if writing == True:
        keyboard.append(WRITING)
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)