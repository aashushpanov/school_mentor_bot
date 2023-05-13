from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.callback_data import CallbackData

from filters.filters import delete_message
from keyboards import callbacks_keyboard, choose_post_call, posts_keyboard
from data.aliases import grades_aliases, posts_aliases
from utils.db.add import add_user
from handlers.menu import reg_call


ru_abc = {'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
          'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', ' '}

is_class_manager_call = CallbackData('is_cm', 'data')
grade_call = CallbackData('grade', 'data')
confirm_registration_call = CallbackData('confirm_registration_data')
restart_registration_call = CallbackData('restart_registration')


def register_registration_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start, reg_call.filter(), chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(get_name, state=Registration.get_name)
    dp.register_message_handler(get_age, state=Registration.get_age)
    dp.register_callback_query_handler(get_post, choose_post_call.filter(), state=Registration.get_post)
    dp.register_callback_query_handler(get_class_manager, is_class_manager_call.filter(),
                                       state=Registration.get_class_manager)
    dp.register_callback_query_handler(get_grade, grade_call.filter(), state=Registration.get_grade)
    dp.register_callback_query_handler(confirm, confirm_registration_call.filter(), state=Registration.confirm)
    dp.register_callback_query_handler(start, restart_registration_call.filter(), state=Registration.confirm)


class Registration(StatesGroup):
    get_name = State()
    get_age = State()
    get_post = State()
    get_class_manager = State()
    get_grade = State()
    confirm = State()


async def start(callback: types.CallbackQuery):
    await callback.answer()
    await delete_message(callback.message)
    await callback.message.answer('Введите Ваше ФИО.')
    await Registration.get_name.set()


async def get_name(message: types.Message, state: FSMContext):
    for lit in message.text.lower():
        if lit not in ru_abc:
            await message.answer('Введите корректные данные')
            return
    await state.update_data(name=message.text)
    await message.answer('Ведите ваш возраст.')
    await Registration.get_age.set()


async def get_age(message: types.Message, state: FSMContext):
    age = message.text
    if age.isalnum() and 10 < int(age) < 100:
        markup = posts_keyboard()
        await state.update_data(age=int(age))
        await message.answer('Выберите должность.', reply_markup=markup)
        await Registration.get_post.set()
    else:
        await delete_message(message)
        await message.answer('Введите корректный возраст.')


async def get_post(callback: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await callback.answer()
    post = callback_data.get('data')
    await delete_message(callback.message)
    await state.update_data(post=post)
    await Registration.get_class_manager.set()
    markup = callbacks_keyboard(texts=['Да', 'Нет'],
                                callbacks=[is_class_manager_call.new(data=1), is_class_manager_call.new(data=0)])
    await callback.message.answer('Вы классный руководитель?', reply_markup=markup)


async def get_class_manager(callback: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await callback.answer()
    await delete_message(callback.message)
    class_manager = int(callback_data.get('data'))
    await state.update_data(class_manager=class_manager)
    await Registration.get_grade.set()
    texts = []
    callbacks = []
    for key, value in grades_aliases.items():
        texts.append(value)
        callbacks.append(grade_call.new(data=key))
    markup = callbacks_keyboard(texts=texts, callbacks=callbacks)
    await callback.message.answer('С какими классами Вы работаете?', reply_markup=markup)


async def get_grade(callback: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await callback.answer()
    await delete_message(callback.message)
    grade = int(callback_data.get('data'))
    await state.update_data(grade=grade)
    data = await state.get_data()
    text = 'Проверьте данные\n\n'
    name = data.get('name')
    post = posts_aliases[data.get('post')]
    grade = grades_aliases[data.get('grade')]
    age = data.get('age')
    class_manager = 'Да' if data.get('class_manager') == 1 else 'Нет'
    text += "ФИО: {}\n" \
            "Возраст {} лет\n" \
            "Должность: {}\n" \
            "Классный руководитель: {}\n" \
            "Классы: {}".format(name, age, post, class_manager, grade)
    markup = callbacks_keyboard(texts=['Все верно', "Начать заново"],
                                callbacks=[confirm_registration_call.new(), restart_registration_call.new()])
    await callback.message.answer(text, reply_markup=markup)
    await Registration.confirm.set()


async def confirm(callback: types.CallbackQuery, state: FSMContext):
    # await callback.answer()
    data = await state.get_data()
    user_id = callback.from_user.id
    name = data.get('name')
    post = data.get('post')
    grade = data.get('grade')
    age = data.get('age')
    is_class_m = data.get('class_manager')
    status = add_user(user_id, name, age, post, is_class_m, grade)
    if status:
        await callback.message.answer('Регистрация завершена, можете вызвать /menu.')
    else:
        await callback.message.answer('Что-то пошло не так')
    await state.finish()
