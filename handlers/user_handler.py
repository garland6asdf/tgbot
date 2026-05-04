from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import currency
from database import get_my_info, insert_into_user_table, remove_user
from keyboards.user_keyboard import (get_back_keyboard, get_currency_keyboard,
                                     get_main_keyboard)
from states import UserDataForm

CURRENCY_MAP = {
    'usd': 'latest/USD',
    'eur': 'latest/EUR',
    'rub': 'latest/RUB',
    'jpy': 'latest/JPY',
    'gbp': 'latest/GBP',
    'cny': 'latest/CNY',
    'cad': 'latest/CAD',
    'aud': 'latest/AUD',
}

router = Router()

@router.message(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        'Я бот разработанный garland!',
        reply_markup=get_main_keyboard()
    )

@router.callback_query(F.data == 'about')
async def button_about(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        'Я показательный бот!👁️👁️',
        reply_markup=get_back_keyboard()
        )


@router.callback_query(F.data == 'user_id')
async def button_user_id(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await callback.answer()
    await callback.message.edit_text(
        f'Твой ID: {user_id}',
        reply_markup=get_back_keyboard()
    )


@router.callback_query(F.data == 'info_about_user')
async def button_info_about_user(callback: types.CallbackQuery):
    await callback.answer()
    username = callback.from_user.username
    info = get_my_info(username)
    if info is not None:
        await callback.message.edit_text(
            f'Твой юз: {info[0]}\n'
            f'Твое имя: {info[1]}\n'
            f'Твой возраст: {info[2]}\n'
            f'Твой номер телефона: {info[3]}\n',
            reply_markup=get_back_keyboard()
        )
    else:
        await callback.message.edit_text(
        'Твоей информации в базе данных нету. Запишись!',
        reply_markup=get_back_keyboard()
        )


@router.callback_query(F.data == "back")
async def back_to_main(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.edit_text(
        'Ку, я бот разработанный Багданом',
        reply_markup=get_main_keyboard()
    )


@router.callback_query(F.data == "removal")
async def removal(callback: types.CallbackQuery):
    await callback.answer()
    tg_username = callback.from_user.username
    remove_user(tg_username)
    await callback.message.edit_text(
        'Ваши данные удалены из базы данных!',
        reply_markup=get_back_keyboard()
    )


@router.callback_query(F.data == 'writing_to_db')
async def button_writing(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    username = callback.from_user.username
    info = get_my_info(username)
    if info is None:
        await state.set_state(UserDataForm.name)
        await callback.message.edit_text(
            'Вы введете ваши данные. Я сохраню их и покажу позже.\n'
            'Введите свое настоящее имя: ',
            reply_markup=get_back_keyboard()
        )
    else:
        await callback.message.edit_text(
            'В базе данных ваша запись уже есть\n'
            'Но вы можете удалить ее, позже перезаписав по новой!',
            reply_markup=get_back_keyboard(remove=True)
        )


@router.message(UserDataForm.name)
async def state_name(message: types.Message, state: FSMContext):
    if 0 >= len(message.text) or len(message.text) > 20:
        await message.answer(
        'Ваше имя либо слишком длинное, либо короткое.\n'
        'Введите снова:',
        reply_markup=get_back_keyboard()
        )
        await state.set_state(UserDataForm.name)
    else:
        await state.update_data(name=message.text)
        await state.set_state(UserDataForm.age)
        await message.answer(
            f'Привет {message.text}! Теперь напиши мне свой возраст: '
        )


@router.message(UserDataForm.age)
async def state_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
    except ValueError:
        await message.answer(
            'Снова введите возраст, но уже цифрами:'
        )
        await state.set_state(UserDataForm.age)
        return
    if age < 5 or age > 110:
        await message.answer(
            'Пожалуйста не врите.\n'
            'Введите возраст заново:',
            reply_markup=get_back_keyboard()
        )
        await state.set_state(UserDataForm.age)
        return
    await state.update_data(age=age)
    await state.set_state(UserDataForm.number)
    await message.answer(
        'А сейчас напиши мне свой номер телефона: '
    )


@router.message(UserDataForm.number)
async def state_number(message: types.Message, state: FSMContext):
    try:
        number = int(message.text)
    except ValueError:
        await message.answer(
            'Снова введите номер, но только цифрами:'
        )
        await state.set_state(UserDataForm.number)
        return
    if len(message.text) < 11 or len(message.text) > 15:
        await message.answer(
            'Номер телефона слишком короткий или длинный\n'
            'Введите заново:'
        )
        await state.set_state(UserDataForm.number)
        return
    await state.update_data(number=message.text)
    data = await state.get_data()
    insert_into_user_table(
        tg_username=message.from_user.username,
        real_name=data['name'],
        age=data['age'],
        number=data['number']
    )
    await message.answer(
        '✅ Данные сохранены!',
        reply_markup=get_back_keyboard()
    )


@router.callback_query(F.data=='currency')
async def button_currency(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        'Относительно какой валюты хотите смотреть курсы?',
        reply_markup=get_currency_keyboard()
    )


@router.callback_query(F.data.in_(CURRENCY_MAP.keys()))
async def button_currency_select(callback: types.CallbackQuery):
    result = currency.main(currency=CURRENCY_MAP[callback.data])
    await callback.answer()
    await callback.message.edit_text(result, reply_markup=get_back_keyboard())
