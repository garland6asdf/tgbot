from aiogram.fsm.state import State, StatesGroup

class UserDataForm(StatesGroup):
    name = State()
    age = State()
    number = State()