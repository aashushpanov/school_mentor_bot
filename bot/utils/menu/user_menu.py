from aiogram.utils.callback_data import CallbackData

from utils.menu.MenuNode import MenuNode, NodeGenerator

place_holder_call = CallbackData('placeholder')
answer_call = CallbackData('answer')
become_mentor_call = CallbackData('become_mentor')
find_mentor_call = CallbackData('find_mentor')
my_data_call = CallbackData('my_data')


def place_holder_func():
    pass


def set_user_menu(main_node: MenuNode = None, root_id='u'):
    # главное меню
    # -------------------------------------------------------
    user_menu = MenuNode(text="Меню педагога", id=root_id)
    if main_node:
        main_node.set_child(user_menu)

    user_menu.set_childs([
        MenuNode('Личная информация'),
        MenuNode('Частые вопросы', callback=answer_call.new()),
        MenuNode('Выбрать наставника', callback=find_mentor_call.new()),
        MenuNode('Стать наставником', callback=become_mentor_call.new()),
        MenuNode('Помощь', callback=place_holder_call.new())
    ])

    user_menu.child(text='Личная информация').set_childs([
        MenuNode('Мои данные', callback=my_data_call.new()),
        MenuNode('Изменить данные', callback=place_holder_call.new()),
        MenuNode('Удалить себя из системы', callback=place_holder_call.new())
    ])

    return user_menu
