import pandas as pd
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageCantBeDeleted

from filters.filters import delete_message
from utils.files import posts


delete_keyboard_call = CallbackData('del')
cansel_event_call = CallbackData('cancel_event')
choose_post_call = CallbackData('choose_role', 'data')


def keyboard_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(delete_keyboard, delete_keyboard_call.filter(), state='*')


async def delete_keyboard(callback: CallbackQuery, state: FSMContext = None):
    if state:
        await state.finish()
    await delete_message(callback.message)


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
