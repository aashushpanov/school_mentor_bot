from .mix import register_mix_handlers
from .cancel import register_cancel_handlers
from .menu import main_menus_handlers


def register_handlers(dp):
    main_menus_handlers(dp)
    register_cancel_handlers(dp)
    register_mix_handlers(dp)

