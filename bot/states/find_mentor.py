import pandas as pd

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from loguru import logger

from data.aliases import posts_aliases
from filters.filters import delete_message
from utils.db.get import get_user, get_mentors
from keyboards.keyboards import switch_keyboard, page_move_call
from utils.menu.menu_structure import user_caption
from utils.menu.user_menu import find_mentor_call


def register_find_mentor_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start, find_mentor_call.filter())
    dp.register_callback_query_handler(turn_page, page_move_call.filter(), state=FindMentor.choose_mentor)


class FindMentor(StatesGroup):
    choose_mentor = State()


def norm_values(value, column):
    match column:
        case 'age':
            return (value - 35) / 15
        case 'is_class_m':
            return value - 0.5
        case 'grade':
            return (value - 1.5) / 1.5
        case _:
            return value


@logger.catch()
async def start(callback: types.CallbackQuery, state: FSMContext):
    logger.info(str(callback.data))
    user = get_user(callback.from_user.id)
    mentors = get_mentors()
    if mentors.empty:
        await callback.answer('Нет доступных наставников', show_alert=True)
        return
    await callback.answer()
    columns_to_norm = ['age', 'is_class_m', 'grade', 'post']
    for column in columns_to_norm:
        mentors[column + '_norm'] = mentors[column].apply(norm_values, args=(column,))
        user[column + '_norm'] = norm_values(user[column], column)
    columns_to_norm = [s + '_norm' for s in columns_to_norm]
    mentors_norm = mentors[columns_to_norm]
    user_norm = user.loc[columns_to_norm]
    corr_column = mentors_norm.corrwith(user_norm, axis=0)
    mentors['corr_column'] = corr_column
    mentors.sort_values(by=['corr_column'], ascending=False)
    total_pages = mentors.shape[0] - 1
    logger.info(str(mentors.shape))
    page = 0
    mentor = mentors.iloc[page]
    markup = switch_keyboard(page, total_pages, cancel_button=True)
    await state.update_data(mentors=mentors)
    await state.update_data(page=page)
    await state.update_data(total_pages=total_pages)
    caption, photo = user_caption(mentor)
    await callback.message.answer_photo(photo=photo, caption=caption, reply_markup=markup)
    await FindMentor.choose_mentor.set()


@logger.catch
async def turn_page(callback: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await callback.answer()
    direction = callback_data.get('data')
    data = await state.get_data()
    page = data.get('page', 0)
    if direction == 'incr':
        page += 1
    else:
        page -= 1
    total_pages = data.get('total_pages')
    mentors = data.get('mentors')
    await state.update_data(page=page)
    mentor = mentors.iloc[page]
    caption, photo = user_caption(mentor)
    markup = switch_keyboard(page, total_pages, cancel_button=True)
    await delete_message(callback.message)
    await callback.message.answer_photo(photo=photo, caption=caption, reply_markup=markup)



