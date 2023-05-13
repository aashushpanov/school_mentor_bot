from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from filters.filters import delete_message
from keyboards.keyboards import cansel_event_call, cancel_event_no_text_call


def register_cancel_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_cancel, commands=['cancel'], state='*')
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state='*')
    dp.register_callback_query_handler(cmd_cancel, cansel_event_call.filter(), state='*')
    dp.register_callback_query_handler(delete_message_from_chat, cancel_event_no_text_call.filter(), state='*')


async def cmd_cancel(message: types.Message | types.CallbackQuery, state: FSMContext):
    await state.finish()
    match message:
        case types.CallbackQuery():
            await message.answer()
            message = message.message
    await message.answer('Действие отменено')
    await delete_message(message)


async def delete_message_from_chat(callback: types.CallbackQuery, state: FSMContext):
    await delete_message(callback.message)
