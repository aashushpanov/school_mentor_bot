from aiogram import types, Dispatcher

from keyboards.keyboards import offer_help_call
from utils.db.get import get_user
from utils.menu.menu_structure import user_caption
from utils.menu.user_menu import my_data_call


def register_mix_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(offer_help, offer_help_call.filter())
    dp.register_callback_query_handler(view_my_data, my_data_call.filter())


async def offer_help(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    await callback.message.delete_reply_markup()
    user = get_user(callback.from_user.id)
    question_id = callback_data.get('q_id')
    message = types.Message(question_id)
    await message.reply('С вашим вопросом готов помочь {} {}'.format(user['name'], user['tg_nick']))


async def view_my_data(callback: types.CallbackQuery):
    await callback.answer()
    user = get_user(callback.from_user.id)
    text, photo = user_caption(user)
    if photo:
        await callback.message.answer_photo(photo=photo, caption=text)
    else:
        await callback.message.answer(text)
