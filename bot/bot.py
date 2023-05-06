import asyncio

from aiogram import executor, Dispatcher

from loader import dp, bot



TIMEOUT = 20*60

def manager():
    pass

async def setup(dp: Dispatcher):
    pass


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