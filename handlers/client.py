from aiogram import types, Bot, F, Router
from aiogram.filters.command import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards.kb import start_kb, admin_kb
from config import ADMINS_ID, FIRST, SECOND, THIRD, FOUR

from db.db import DataBase

db = DataBase()

class Aplication(StatesGroup):
    firts = State()
    second = State()
    third = State()
    four = State()

Rclient = Router()

@Rclient.message(CommandStart())
async def start_cmd(message: types.Message):
    if f"@{message.from_user.username}" in ADMINS_ID:
        await message.answer('Добро пожаловать', reply_markup=admin_kb())
    else:
        await message.answer('''
                             🟢Добро пожаловать в <b>team name!</b>🟢
                             
<em>Для подачи заявки нажмите кнопку ниже</em>''', reply_markup=start_kb(), parse_mode='HTML')
    
@Rclient.callback_query(F.data == 'application')
async def application_add(callback: types.CallbackQuery, state: FSMContext):
    
    if await db.select_by_id(callback.from_user.id):
        await callback.message.edit_text('Вы уже подавали заявку')
    else:
        await callback.message.answer(FIRST)
        await state.set_state(Aplication.firts)
        await callback.answer()
    
@Rclient.message(Aplication.firts)
async def firts_state(message: types.Message, state: FSMContext):
    await state.update_data(username=message.from_user.username)
    await state.update_data(chat_id=message.from_user.id)
    await state.update_data(first=message.text)
    await message.answer(SECOND)
    await state.set_state(Aplication.second)
    
@Rclient.message(Aplication.second)
async def second_state(message: types.Message, state: FSMContext):
    await state.update_data(second=message.text)
    await message.answer(THIRD)
    await state.set_state(Aplication.third)
    
@Rclient.message(Aplication.third)
async def firts_state(message: types.Message, state: FSMContext):
    await state.update_data(third=message.text)
    await message.answer(SECOND)
    await state.set_state(Aplication.four)
    
@Rclient.message(Aplication.four)
async def firts_state(message: types.Message, state: FSMContext):
    await state.update_data(four=message.text)
    await message.answer("Ожидайте. Ваша заявка будет рассмотрена в ближайшее время")
    await db.add_user(await state.get_data())