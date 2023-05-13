import pytz
import datetime as dt
from fone_task.updates import update_question_validity


async def manager():
    """
    Он обновляет базу данных, получает пользователей, которые должны быть уведомлены в настоящее время, получает уведомления
    для этих пользователей и отправляет уведомления.
    """
    hour = dt.datetime.now(pytz.timezone('Europe/Moscow')).time().hour

    if 1 <= hour <= 2:
        update_question_validity()
