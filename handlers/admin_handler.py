import asyncio
from aiogram import Router, types, F
from aiogram.filters import Command
from keyboards.admin_keyboard import get_main_admin_keyboard
from keyboards.user_keyboard import get_back_keyboard

from cfg import ADMIN_IDS
from database import get_all_users
router = Router()

@router.callback_query(F.data == 'admin_panel')
async def button_for_admins(callback: types.CallbackQuery):
    await callback.answer()
    id = callback.from_user.id
    if id in ADMIN_IDS:
        await callback.message.edit_text(
            'Панель управления админа',
            reply_markup=get_main_admin_keyboard()
        )
    else:
        await callback.message.edit_text(
            'Ты не админ божж 🤣\n'
            'Пиздуй в меню или бей челом батюшке Богдану, чтоб добавил в админы 🥰',
            reply_markup=get_back_keyboard()
    )

@router.callback_query(F.data == 'all_notes')
async def button_all_notes(callback: types.CallbackQuery):
    await callback.answer()
    info = get_all_users()
    text = "Список пользователей:\n\n"
    for index, item in enumerate(info):
        username, name, age, number = item
        text+=f'{index+1}. Юз: {username}\n'
        text+=f'\tИмя: {name}\n'
        text+=f'\tВозраст: {age}\n'
        text+=f'\tНомер телефона: {number}\n'
    await callback.message.edit_text(
        text,
        reply_markup=get_back_keyboard()
    )


