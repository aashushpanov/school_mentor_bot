from aiogram.utils.callback_data import CallbackData

from utils.menu.MenuNode import MenuNode, NodeGenerator

get_topic_q_call = CallbackData('get_topic_q')


def set_topic_menu():
    topic_menu = MenuNode(text='Меню', id='t')

    topic_menu.set_childs([
        MenuNode('Посмотреть вопросы', callback=get_topic_q_call.new())
    ])

    return topic_menu