from aiogram import Dispatcher
from aiogram import types
from aiogram.utils.callback_data import CallbackData

from keyboards import yes_no_keyboard

from filters.filters import IsExist, TimeAccess
from utils.menu.MenuNode import move
from utils.db.get import get_access
from utils.menu.menu_structure import user_menu, list_menu

reg_call = CallbackData('reg_call')


def main_menus_handlers(dp: Dispatcher):
    dp.register_message_handler(reg_suggestion, IsExist(0), commands=['menu'], chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(show_main_menu, IsExist(1), commands=['menu'],
                                chat_type=types.ChatType.PRIVATE, state='*')
    dp.register_callback_query_handler(list_menu, move.filter(), TimeAccess(), state='*')


async def reg_suggestion(message: types.Message):
    await message.answer(text='Для доступа к функциям необходимо зарегистрироваться. Сделать это сейчас?',
                         reply_markup=yes_no_keyboard(reg_call.new()))


async def show_main_menu(message: types.Message, state=None):
    current_state = await state.get_state()
    if current_state:
        await state.finish()
        await message.answer('Действие отменено')
    match get_access(user_id=message.from_user.id):
        case 3:
            menu = user_menu
        case 2:
            menu = user_menu
        case _:
            menu = user_menu
    await list_menu(message, menu=menu, title='Меню')
