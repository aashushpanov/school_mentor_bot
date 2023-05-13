from aiogram import Dispatcher

from .find_mentor import register_find_mentor_handlers
from .ask_question import register_ask_question_handlers
from .registration import register_registration_handlers
from .become_mentor import register_mentor_handlers


def register_states_handlers(dp: Dispatcher):
    register_registration_handlers(dp)
    register_ask_question_handlers(dp)
    register_mentor_handlers(dp)
    register_find_mentor_handlers(dp)
