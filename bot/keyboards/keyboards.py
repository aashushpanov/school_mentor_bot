import pandas as pd
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageCantBeDeleted

from filters.filters import delete_message
from utils.files import posts
from utils.menu import MenuNode
from utils.menu.MenuNode import move

delete_keyboard_call = CallbackData('del')
cansel_event_call = CallbackData('cancel_event')
cancel_event_no_text_call = CallbackData('cancel_event_no_text')
choose_post_call = CallbackData('choose_role', 'data')
pages_keyboard_call = CallbackData('pk', 'data')
page_move_call = CallbackData('page_move', 'data')
pages_back_call = CallbackData('pages_back')
offer_help_call = CallbackData('offer_help', 'q_id')
delete_message_call = CallbackData('delete_message')


def keyboard_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(delete_keyboard, delete_keyboard_call.filter(), state='*')


async def delete_keyboard(callback: CallbackQuery, state: FSMContext = None):
    if state:
        await state.finish()
    await delete_message(callback.message)


def cancel_keyboard(cancel_text=None, no_text=False):
    markup = InlineKeyboardMarkup()
    cancel_text = cancel_text if cancel_text else '\U0000274C Отмена'
    if no_text:
        callback = cancel_event_no_text_call.new()
    else:
        callback = cansel_event_call.new()
    markup.insert(InlineKeyboardButton(text=cancel_text, callback_data=callback))
    return markup


def posts_keyboard():
    markup = InlineKeyboardMarkup()
    for _, post in posts.iterrows():
        code = post['code']
        name = post['name']
        markup.insert(InlineKeyboardButton(text=name, callback_data=choose_post_call.new(data=code)))
    return markup


def callbacks_keyboard(texts: list, callbacks: list, cansel_button: bool = False):
    """
    Эта функция создает встроенную разметку клавиатуры с кнопками, которые могут вызывать обратный вызов
    или открывать URL-адрес, а также включает дополнительную кнопку отмены.
    
    :param texts: Список строк, представляющих текст, который будет отображаться на кнопках
    :type texts: list
    :param callbacks: Список строк данных обратного вызова или URL-адресов, которые будут связаны с
    каждой кнопкой на клавиатуре
    :type callbacks: list
    :param cansel_button: Логический параметр, определяющий, включать ли кнопку отмены на клавиатуру.
    Если установлено значение True, на клавиатуру будет добавлена кнопка отмены. Если установлено
    значение False, кнопка отмены не будет добавлена, defaults to False
    :type cansel_button: bool (optional)
    :return: экземпляр класса InlineKeyboardMarkup с кнопками, созданными из списков texts и callbacks.
    Если `cansel_button` равно `True`, в разметку также добавляется кнопка отмены.
    """
    if len(texts) != len(callbacks) and len(callbacks) != 0:
        raise KeyError
    button_dict = dict(zip(texts, callbacks))
    markup = InlineKeyboardMarkup(row_width=1)
    for text, callback in button_dict.items():
        if isinstance(callback, str) and isinstance(text, str):
            if callback.__contains__('://'):
                markup.insert(InlineKeyboardButton(text=text, url=callback))
            else:
                markup.insert(InlineKeyboardButton(text=text, callback_data=callback))
        else:
            raise TypeError
    if cansel_button:
        markup.insert(InlineKeyboardButton(text='\U0000274C Отмена', callback_data=cansel_event_call.new()))
    return markup


def yes_no_keyboard(callback):
    markup = InlineKeyboardMarkup()

    markup.insert(InlineKeyboardButton(text='\U00002705 Да', callback_data=callback))
    markup.insert(InlineKeyboardButton(text='\U0000274C	Нет', callback_data=delete_keyboard_call.new()))

    return markup


async def tree_menu_keyboard(menu_node: MenuNode, callback: CallbackQuery = None, data=None):
    if callback is not None:
        row_width = int(callback.data.split(':')[-1])
    else:
        row_width = 1
    markup = InlineKeyboardMarkup(row_width=row_width)

    async for _, text, node_callback in menu_node.childs_data(callback=callback, data=data):
        if node_callback.__contains__('://'):
            markup.insert(InlineKeyboardButton(text=text, url=node_callback))
        else:
            markup.insert(InlineKeyboardButton(text=text, callback_data=node_callback))

    if menu_node.parent:
        markup.insert(
            InlineKeyboardButton(text="\U00002B05 Назад",
                                 callback_data=move.new(action='u', node=menu_node.id, data='', width=1)))

    return markup


def pages_keyboard(list_of_instance: pd.DataFrame, callback_column: str, text_column: str, page: int, height: int = 5,
                   cansel_button=False, back_button=False, back_button_text=None):
    """
    Он принимает фрейм данных, столбец для использования в качестве данных обратного вызова, столбец для использования в
    качестве текста, текущую страницу и количество строк на странице и возвращает клавиатуру со строками фрейма данных в
    качестве кнопок.

    :param cansel_button:
    :param list_of_instance: pd.DataFrame — кадр данных, содержащий данные, которые вы хотите отобразить
    :type list_of_instance: pd.DataFrame
    :param callback_column: столбец в кадре данных, который содержит данные обратного вызова
    :type callback_column: str
    :param text_column: столбец в кадре данных, содержащий текст, который будет отображаться на кнопке
    :type text_column: str
    :param page: int - номер страницы
    :type page: int
    :param height: количество строк для отображения на странице, defaults to 5
    :type height: int (optional)
    :return: Объект InlineKeyboardMarkup
    """
    if list_of_instance.shape[0] - (page + 1) * height == 1:
        top = (page + 1) * height + 1
        last_page = True
    else:
        top = (page + 1) * height
        last_page = False
    if list_of_instance.shape[0] < (page + 1) * height:
        last_page = True
    page_list = list_of_instance.iloc[height * page:top]
    markup = InlineKeyboardMarkup(row_width=1)
    for _, row in page_list.iterrows():
        markup.insert(InlineKeyboardButton(text=row[text_column],
                                           callback_data=pages_keyboard_call.new(data=row[callback_column])))
    left_btn = None
    right_btn = None
    if page != 0:
        left_btn = InlineKeyboardButton(text='\U000025C0', callback_data=page_move_call.new(data='decr'))
    if not last_page:
        right_btn = InlineKeyboardButton(text='\U000025B6', callback_data=page_move_call.new(data='incr'))
    if right_btn is None and left_btn is None:
        pass
    elif right_btn and left_btn:
        markup.row(left_btn, right_btn)
    else:
        if left_btn:
            btn = left_btn
        else:
            btn = right_btn
        markup.row(btn)
    if cansel_button:
        markup.insert(InlineKeyboardButton(text='\U0000274C Отмена', callback_data=cansel_event_call.new()))
    if back_button:
        button_text = back_button_text if back_button_text is not None else 'Назад'
        markup.insert(InlineKeyboardButton(text=button_text, callback_data=pages_back_call.new()))
    return markup


def offer_help_keyboard(question_id):
    markup = InlineKeyboardMarkup()
    markup.insert(InlineKeyboardButton(text='Готов помочь', callback_data=offer_help_call.new(q_id=question_id)))
    return markup


def switch_keyboard(page, total_pages, cancel_button=False):
    markup = InlineKeyboardMarkup(row_width=1)
    left_btn = None
    right_btn = None
    if page != 0:
        left_btn = InlineKeyboardButton(text='\U000025C0', callback_data=page_move_call.new(data='decr'))
    if page != total_pages:
        right_btn = InlineKeyboardButton(text='\U000025B6', callback_data=page_move_call.new(data='incr'))
    if right_btn and left_btn:
        markup.row(left_btn, right_btn)
    else:
        btn = None
        if left_btn:
            btn = left_btn
        elif right_btn:
            btn = right_btn
        if btn:
            markup.row(btn)
    if cancel_button:
        markup.insert(InlineKeyboardButton(text='\U0000274C Отмена', callback_data=cansel_event_call.new()))
    return markup

