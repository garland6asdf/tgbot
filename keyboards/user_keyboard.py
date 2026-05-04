from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

BACK = [InlineKeyboardButton(text='Вернуться в главное меню↩️', callback_data='back')]
REMOVAL = [InlineKeyboardButton(text='Удалить❌', callback_data='removal')]

def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton(text='О боте🧐', callback_data='about')],
        [InlineKeyboardButton(text='Записать свои данные📝', callback_data='writing_to_db')],
        [InlineKeyboardButton(text='Узнать свой ID🔐', callback_data='user_id')],
        [InlineKeyboardButton(text='Моя информация📫', callback_data='info_about_user')],
        [InlineKeyboardButton(text='Валюта💰', callback_data='currency')],
        [InlineKeyboardButton(text='Для админов👔', callback_data='admin_panel')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_back_keyboard(remove=False):
    keyboard = [
        BACK,
    ]
    if remove == True: 
        keyboard.insert(
            0,
            REMOVAL
        ) # Тут именно инсерт, чтобы была приятнее внешка менюшки
    return InlineKeyboardMarkup(inline_keyboard=keyboard) # По логике сначала кнопка удалить, потом уже "главное меню"


def get_currency_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(text='🗽USD🦅', callback_data='usd'),
            InlineKeyboardButton(text='📈EUR🏛️', callback_data='eur')
        ],
        [
            InlineKeyboardButton(text='📉RUB👎', callback_data='rub'),
            InlineKeyboardButton(text='🪭JPY🏮', callback_data='jpy')
        ],
        [
            InlineKeyboardButton(text='💂‍♂️GBP🫖', callback_data='gbp'),
            InlineKeyboardButton(text='🥢CNY🧧', callback_data='cny')
        ],
        [
            InlineKeyboardButton(text='❄️CAD🍁', callback_data='cad'),
            InlineKeyboardButton(text='🦘AUD☀️', callback_data='aud')
        ],
        BACK
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)