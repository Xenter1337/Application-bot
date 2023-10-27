from aiogram.utils.keyboard import InlineKeyboardBuilder

def start_kb(): 
    
    ikb = InlineKeyboardBuilder()
    ikb.button(text='Подать заявку💬', callback_data='application')
    
    return ikb.as_markup()

def admin_kb():
    ikb = InlineKeyboardBuilder()
    
    ikb.button(text='Просмотр заявок✏️', callback_data='application_list')
    
    return ikb.as_markup()

def app_kb():
    
    ikb = InlineKeyboardBuilder()
    ikb.button(text='Принять✅', callback_data='accept')
    ikb.button(text='Отклонить❌', callback_data='decline')
    
    return ikb.as_markup()









