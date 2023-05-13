from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.callback_data import CallbackData

from keyboards import yes_no_keyboard
from utils.db.add import delete_user
from utils.menu.user_menu import delete_data_call


def register_mix_state_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(ask_delete_confirm, delete_data_call.filter())


class DeleteYourself(StatesGroup):
    ask_delete_confirm = State()


confirm_delete_yourself_call = CallbackData('confirm_delete_yourself')


async def ask_delete_confirm(callback: types.CallbackQuery):
    await callback.answer()
    markup = yes_no_keyboard(callback=confirm_delete_yourself_call.new())
    await callback.message.answer('Вы точно хотите удалить себя из системы?',
                                  reply_markup=markup)
    await DeleteYourself.ask_delete_confirm.set()


async def confirm_delete_user(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id
    status = delete_user(user_id)
    if status:
        await callback.message.answer('Вы удалены из системы')
    else:
        await callback.message.answer('Что-то пошло не так.')
    await state.finish()
