import pandas as pd

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from loguru import logger

from filters.filters import delete_message
from loader import bot

from utils.db.get import get_user
from keyboards.keyboards import pages_keyboard, page_move_call, pages_keyboard_call, cancel_keyboard, \
    offer_help_keyboard, pages_back_call
from utils.menu.user_menu import answer_call
from utils.files import topics, questions, topic_chats
from utils.db.add import add_question


class AskQuestion(StatesGroup):
    choose_topic = State()
    choose_question = State()
    ask_moderators = State()
    ask_head = State()


def register_ask_question_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start, answer_call.filter())
    dp.register_callback_query_handler(turn_topic_page, page_move_call.filter(), state=AskQuestion.choose_topic)
    dp.register_callback_query_handler(choose_question, pages_keyboard_call.filter(), state=AskQuestion.choose_topic)
    dp.register_callback_query_handler(turn_question_page, page_move_call.filter(), state=AskQuestion.choose_question)
    dp.register_callback_query_handler(start, pages_back_call.filter(), state=AskQuestion.choose_question)
    dp.register_callback_query_handler(get_question, pages_keyboard_call.filter(), state=AskQuestion.choose_question)
    dp.register_message_handler(ask_head, state=AskQuestion.ask_head)


async def start(callback: types.CallbackQuery, state: FSMContext):
    await delete_message(callback.message)
    markup = pages_keyboard(topics, 'code', 'name', 0)
    await callback.message.answer('Выберите категорию', reply_markup=markup)
    await state.update_data(page=0)
    await AskQuestion.choose_topic.set()


async def turn_topic_page(callback: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await callback.answer()
    direction = callback_data.get('data')
    data = await state.get_data()
    page = data.get('page', 0)
    if direction == 'incr':
        page += 1
    else:
        page -= 1
    await state.update_data(page=page)
    markup = pages_keyboard(topics, 'code', 'name', page)
    await callback.message.edit_reply_markup(markup)


async def choose_question(callback: types.CallbackQuery, state: FSMContext, callback_data: dict):
    topic = callback_data.get('data')
    if topic != 'nf':
        topic_questions = questions[questions['topic'] == topic]
        await state.update_data(page=0)
        await state.update_data(topic=topic)
        markup = pages_keyboard(topic_questions, 'rang', 'question', 0, back_button=True, back_button_text='К темам')
        await callback.message.edit_text('Выберите вопрос', reply_markup=markup)
        await AskQuestion.choose_question.set()
    else:
        await delete_message(callback.message)
        markup = cancel_keyboard()
        await callback.message.answer('Опишите свой вопрос ниже.', reply_markup=markup)
        await AskQuestion.ask_head.set()
    

async def turn_question_page(callback: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await callback.answer()
    direction = callback_data.get('data')
    data = await state.get_data()
    page = data.get('page', 0)
    topic = data.get('topic')
    topic_questions = questions[questions['topic'] == topic]
    if direction == 'incr':
        page += 1
    else:
        page -= 1
    await state.update_data(page=page)
    markup = pages_keyboard(topic_questions, 'rang', 'question', page, back_button=True, back_button_text='К темам')
    await callback.message.edit_reply_markup(markup)


async def get_question(callback: types.CallbackQuery, state: FSMContext, callback_data: dict):
    rang = callback_data.get('data')
    data = await state.get_data()
    topic = data.get('topic')
    if rang == 'nf':
        markup = cancel_keyboard(no_text=True)
        await callback.message.answer('Опишите свой вопрос ниже.', reply_markup=markup)
    else:
        await return_common_answer(callback.message, topic, int(rang), state)


async def return_common_answer(message, topic, question_rang, state):
    answer = questions[(questions['topic'] == topic) & (questions['rang'] == question_rang)]['answer'].iloc[0]
    markup = cancel_keyboard(cancel_text='Понятно', no_text=True)
    await message.answer(answer, reply_markup=markup)


async def ask_head(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = get_user(user_id)
    data = await state.get_data()
    topic = data.get('topic')
    message_id = message.message_id
    question = "{} спрашивает:\n{}".format(user['name'], message.text)
    markup = None
    if topic == 'nf':
        topic = 'moderators'
    chat_id = topic_chats[topic_chats['topic'] == topic]['chat_id'].iloc[0]
    status, question_id = add_question(message_id, user_id, question, topic)
    if topic != 'moderator':
        markup = offer_help_keyboard(question_id)
    if status:
        await bot.send_message(chat_id=chat_id, text=question, reply_markup=markup)
        await message.answer('Ваш вопрос отправлен.')
    else:
        await message.answer('Что-то пошло не так.')
    await state.finish()
