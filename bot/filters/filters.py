import datetime as dt

from aiogram import types
from aiogram.dispatcher.filters import Filter


async def delete_message(message: types.Message):
    delta = abs(dt.datetime.now() - message.date)
    access = 2 - delta.seconds/(3600*24) - delta.days
    if access > 0:
        await message.delete()
    else:
        await message.edit_text('Удалено')
