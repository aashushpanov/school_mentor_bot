from aiogram.utils.callback_data import CallbackData

from utils.menu.MenuNode import MenuNode, NodeGenerator

place_holder_call = CallbackData('placeholder')
answer_call = CallbackData('answer')
become_mentor_call = CallbackData('become_mentor')
find_mentor_call = CallbackData('find_mentor')
my_data_call = CallbackData('my_data')
change_name_call = CallbackData('change_name')
change_photo_call = CallbackData('change_photo')
change_direction_call = CallbackData('change_direction')
change_bio_call = CallbackData('change_bio')
delete_data_call = CallbackData('delete_data')


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
        MenuNode('Изменить данные'),
        MenuNode('Удалить себя из системы', callback=delete_data_call.new())
    ])

    user_menu.child(text='Личная информация').child(text='Изменить данные').set_childs([
        MenuNode('Имя', change_name_call.new()),
        MenuNode('Фотографию', change_photo_call.new()),
        MenuNode('Направление', change_direction_call.new()),
        MenuNode('О себе', change_bio_call.new())
    ])

    return user_menu
