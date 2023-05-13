from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.callback_data import CallbackData

from loader import bot

from utils.db.get import get_access
from utils.db.add import add_mentor
from utils.menu.user_menu import become_mentor_call
from filters.filters import delete_message
from utils.db.add import confirm_mentor
from utils.db.get import is_mentor_already_registered, get_user
from utils.files import topic_chats
from keyboards.keyboards import callbacks_keyboard


mentor_proposal_call = CallbackData('mentor_proposal', 'a', 'id')


def register_mentor_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start, become_mentor_call.filter())
    dp.register_message_handler(get_photo, content_types=types.ContentTypes.PHOTO, state=BecomeMentor.get_photo)
    dp.register_message_handler(get_direction, state=BecomeMentor.get_direction)
    dp.register_message_handler(get_bio, state=BecomeMentor.get_bio)


class BecomeMentor(StatesGroup):
    get_photo = State()
    get_direction = State()
    get_bio = State()


async def start(callback: types.CallbackQuery):
    access = get_access(callback.from_user.id)
    await delete_message(callback.message)
    if access == 1:
        await callback.answer('Вы уже наставник.', show_alert=True)
    else:
        await callback.answer()
        if is_mentor_already_registered(user_id=callback.from_user.id) == 0:
            await send_mentor_proposal(callback.from_user.id)
            return
        await callback.message.answer('Загрузите свою фотографию')
        await BecomeMentor.get_photo.set()


async def get_photo(message: types.Message, state: FSMContext):
    if photo := message.photo:
        file_id = photo[-1].file_id
        await state.update_data(file_id=file_id)
        await message.answer('Чем вы занимаетесь в школе?')
        await BecomeMentor.get_direction.set()


async def get_direction(message: types.Message, state: FSMContext):
    direction = message.text
    await state.update_data(direction=direction)
    await message.answer('Разкажите о себе')
    await BecomeMentor.get_bio.set()


async def get_bio(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    tg_nick = '@' + message.from_user.username
    bio = message.text
    data = await state.get_data()
    file_id = data.get('file_id')
    direction = data.get('direction')
    status = add_mentor(user_id, tg_nick, file_id, direction, bio)
    if status:
        await message.answer('Вы зарегистрированы как наставник')
    else:
        await message.answer('Что-то пошло не так')
    await state.finish()


async def send_mentor_proposal(user_id):
    user = get_user(user_id)
    name = user['name']
    text = "{} хочет стать наставником.".format(name)
    chat_id = topic_chats[topic_chats['topic'] == 'mentors']['chat_id'].iloc[0]
    markup = callbacks_keyboard(texts=['Принять', 'Отклонить'],
                                callbacks=[mentor_proposal_call.new(a='g', id=user_id),
                                           mentor_proposal_call.new(a='r', id=user_id)])
    await bot.send_message(chat_id, text, reply_markup=markup)


async def confirm_from_moderators(callback: types.CallbackQuery, callback_data: dict):
    await callback.message.delete_reply_markup()
    if callback_data.get('a') == 'g':
        status = confirm_mentor(callback_data.get('id'))
        if status:
            await callback.message.answer('Заявка подтверждена')
        else:
            await callback.message.answer('Что-то пошло не так.')
    else:
        await callback.message.answer('Заявка отклонена')
