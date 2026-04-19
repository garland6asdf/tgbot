import asyncio
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards.user_keyboard import get_back_keyboard, get_main_keyboard
from states import UserDataForm

from database import insert_into_user_table, get_my_info


router = Router()


@router.message(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext):
    state.clear()
    await message.answer(
        'Ку, я бот разработанный багданом',
        reply_markup=get_main_keyboard()
    )


@router.callback_query(F.data == 'about')
async def button_about(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        'Я показательный бот. Вот и все нах',
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
        await callback.message.answer(
            f'Твой юз: {info[0]}\n'
            f'Твое имя: {info[1]}\n'
            f'Твой возраст: {info[2]}\n'
            f'Твой номер телефона: {info[3]}\n',
            reply_markup=get_back_keyboard()
        )
    else:
        await callback.message.answer(
        'Твоей информации в базе данных нету. Запишись!',
        reply_markup=get_back_keyboard()
        )

@router.callback_query(F.data == "back")
async def back_to_main(callback: types.CallbackQuery, state: FSMContext):
    state.clear()
    await callback.answer()
    await callback.message.edit_text(
        'Ку, я бот разработанный Багданом',
        reply_markup=get_main_keyboard()
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
            'Сорян, но в базе данных твоя запись уже есть. Сделать новую не получится(((',
            reply_markup=get_back_keyboard()
        )


@router.message(UserDataForm.name)
async def state_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(UserDataForm.age)
    await message.answer(
        f'Привит {message.text}! Теперь напиши мне свой возраст: '
    )


@router.message(UserDataForm.age)
async def state_age(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await state.set_state(UserDataForm.number)
    await message.answer(
        f'А щас напиши мне свой номер телефона: '
    )


@router.message(UserDataForm.number)
async def state_number(message: types.Message, state: FSMContext):
    await state.update_data(number=int(message.text))
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