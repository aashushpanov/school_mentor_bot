import asyncio

from aiogram import executor, Dispatcher

from handlers import register_handlers
from commands.user import set_user_commands


from loader import dp, bot
from states.registration import register_registration_handlers


TIMEOUT = 20*60


def manager():
    pass


async def setup(dp: Dispatcher):
    register_registration_handlers(dp)
    register_handlers(dp)
    await set_user_commands(bot)


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(TIMEOUT, repeat, coro, loop)


if __name__ == '__main__':
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.call_later(TIMEOUT, repeat, manager, loop)
        executor.start_polling(dp, loop=loop, skip_updates=False, on_startup=setup)
    except KeyboardInterrupt:
        pass