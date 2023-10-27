from aiogram import types, F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from handlers.client import db
from keyboards.kb import app_kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from config import CHAT_LINK

class AppCheck(StatesGroup):
    check = State()

router = Router()

@router.callback_query(F.data == 'application_list')
async def app_list(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AppCheck.check)
    res = await db.select_app()
    print(res)
    if res:
        await callback.message.edit_text(f"""
                Заявка <code>@{res['username']}</code>
                
    1. {res['first']}
    2. {res['second']}
    3. {res['third']}
    4. {res['four']}""", parse_mode='HTML', reply_markup=app_kb())
        
        await state.update_data(our=res['chat_id'])
    else:
        await callback.message.edit_text('Заявок нет!')
    await callback.answer()
    
@router.callback_query(F.data == 'accept')
async def accept_app(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    chat_id = await state.get_data()
    await db.update_status(chat_id['our'], 'accept')
    try:
        await bot.send_message(chat_id=chat_id['our'], text=f'''Ваша заявка была одобрена.✅
                               
Ссылка на чат: {CHAT_LINK}
''')
    except Exception as ex:
        await callback.message.answer(f'[INFO] {ex}')
    # делаем что хотим
    await app_list(callback, state)
    await callback.answer()
    
@router.callback_query(F.data == 'decline')
async def accept_app(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    chat_id = await state.get_data()
    print(chat_id)
    try:
        await bot.send_message(chat_id=str(chat_id['our']), text='Ваша заявка была отклонена❌')
    except Exception as ex:
        await callback.message.answer(f'[INFO] {ex}')
    await db.update_status(chat_id['our'], 'decline')
    await app_list(callback, state)
    await callback.answer()

