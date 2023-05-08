from aiogram import Dispatcher
from aiogram import types
from aiogram.utils.callback_data import CallbackData

from keyboards import yes_no_keyboard

reg_call = CallbackData('reg_call')


def main_menus_handlers(dp: Dispatcher):
    dp.register_message_handler(reg_suggestion, commands=['menu'], chat_type=types.ChatType.PRIVATE)


async def reg_suggestion(message: types.Message):
    await message.answer(text='Для доступа к функциям необходимо зарегистрироваться. Сделать это сейчас?',
                         reply_markup=yes_no_keyboard(reg_call.new()))