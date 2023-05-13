from aiogram.utils.callback_data import CallbackData

from utils.menu.MenuNode import MenuNode, NodeGenerator
from utils.menu.generator_functions import get_files



non_answered_q_call = CallbackData('non_answered_q')


def set_moderator_menu():
    moderator_menu = MenuNode(text='Меню модератора', id='m')

    moderator_menu.set_childs([
        MenuNode(text='Неотвеченные вопросы', callback=non_answered_q_call.new()),
        NodeGenerator(text='Выгрузки', func=get_files)
    ])

    moderator_menu.child(text='Выгрузки').add_blind_node('dl_opt')

    return moderator_menu