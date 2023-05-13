from aiogram import types

from keyboards.keyboards import tree_menu_keyboard
from utils.menu.user_menu import set_user_menu


user_menu = set_user_menu(root_id='user')

menu_childs = user_menu.all_childs()


async def list_menu(callback: types.CallbackQuery | types.Message, callback_data: dict = None, menu=None, title=''):
    match callback:
        case types.Message():
            markup = await tree_menu_keyboard(menu)
            await callback.answer(title, reply_markup=markup)
        case types.CallbackQuery():
            await callback.answer()
            if callback_data.get('action') == "d":
                next_node = menu_childs.get(callback_data.get('node'))
            elif callback_data.get('action') == 'u':
                next_node = menu_childs.get(callback_data.get('node')).parent
            else:
                raise KeyError
            data = callback_data.get('data')
            markup = await tree_menu_keyboard(next_node, callback, data)
            text = next_node.text
            await callback.message.edit_text(text=text, reply_markup=markup)
