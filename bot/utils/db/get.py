import pandas as pd
from loguru import logger

from utils.db.connect import database


@logger.catch
def get_access(user_id: int) -> object:
    """
    Получает уровень доступа пользователя из базы данных

    :param user_id: Идентификатор пользователя
    :type user_id: int
    :return: Уровень доступа пользователя.
    """
    with database() as (cur, conn, status):
        sql = "SELECT is_admin FROM users WHERE user_id = %s"
        cur.execute(sql, [user_id])
        result = cur.fetchone()
    return result[0] if result else 0


@logger.catch
async def is_exist(user_id):
    """
    Он проверяет, существует ли пользователь в базе данных

    :param user_id: Идентификатор пользователя
    :return: 1 если результат иначе 0
    """
    result = 0
    with database() as (cur, conn, status):
        sql = "SELECT name FROM users WHERE user_id = %s"
        cur.execute(sql, [user_id])
        result = cur.fetchone()
    return 1 if result else 0


@logger.catch
def get_user(user_id) -> pd.Series:
    with database() as (cur, conn, status):
        sql = "SELECT name, age, post, is_class_m, grade, is_admin, photo_id, direction, bio, tg_nick" \
              " FROM USERS WHERE user_id = %s"
        cur.execute(sql, [user_id])
        result = cur.fetchone()
        index = ['name', 'age', 'post', 'is_class_m', 'grade', 'is_admin', 'photo_id', 'direction', 'bio', 'tg_nick']
        data = pd.Series(result, index=index)
    return data


@logger.catch
def get_mentors():
    with database() as (cur, conn, status):
        sql = "SELECT name, age, is_class_m, grade, post, direction, bio, photo_id, tg_nick, is_admin FROM USERS" \
              " WHERE is_admin = 2"
        cur.execute(sql, [])
        result = cur.fetchall()
        columns = ['name', 'age', 'is_class_m', 'grade', 'post', 'direction', 'bio', 'photo_id', 'tg_nick', 'is_admin']
        data = pd.DataFrame(result, columns=columns)
    return data


@logger.catch
def is_mentor_already_registered(user_id):
    with database() as (cur, conn, status):
        sql = "SELECT is_confirmed FROM users WHERE user_id = %s"
        cur.execute(sql, [user_id])
        result = cur.fetchone()
    return result is not None


@logger.catch
def get_all_non_answered_q():
    with database() as (cur, conn, status):
        sql = "SELECT from_user, question, question_date, topic FROM question WHERE is_active = 0"
        cur.execute(sql, [])
        result = cur.fetchall()
        columns = ['from_user', 'question', 'question_date', 'topic']
        data = pd.DataFrame(result, columns=columns)
    return data


@logger.catch
def get_topic_non_answered_q(topic):
    with database() as (cur, conn, status):
        sql = "SELECT id, from_user, question_text, question_date FROM question WHERE answered_user = 'none' AND topic = %s"
        cur.execute(sql, [topic])
        result = cur.fetchall()
        columns = ['id', 'from_user', 'question', 'question_date']
        data = pd.DataFrame(result, columns=columns)
    return data