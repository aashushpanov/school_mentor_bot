import pandas as pd
from psycopg2.extras import Json
import datetime as dt
from loguru import logger

from pandas import DataFrame, Series

from .connect import database


@logger.catch
def add_user(user_id, name, age, post, is_class_m, grade):
    """
    Эта функция добавляет нового пользователя в базу данных с указанным идентификатором пользователя,
    именем, должностью, статусом членства в классе и оценкой.
    
    :param user_id: Уникальный идентификатор пользователя, добавляемого в базу данных
    :param name: Имя пользователя, добавляемого в базу данных
    :param post: Параметр post, вероятно, относится к положению или роли пользователя в системе или
    организации. Это может быть что-то вроде «студент», «учитель», «администратор» или любое другое
    соответствующее обозначение
    :param is_class_m: is_class_m — логическое значение, указывающее, является ли пользователь монитором
    класса или нет. Если значение равно True, это означает, что пользователь является монитором класса,
    а если значение равно False, это означает, что пользователь не является монитором класса
    :param grade: Параметр оценки, вероятно, относится к академическому уровню пользователя,
    добавляемого в базу данных
    :return: статус подключения к базе данных после выполнения SQL-запроса для вставки нового
    пользователя в таблицу «users».
    """
    with database() as (curr, conn, status):
        sql = "INSERT INTO users (user_id, name, age, post, is_class_m, grade, is_admin)" \
              " VALUES (%s, %s, %s, %s, %s, %s, 0)"
        curr.execute(sql, [user_id, name, age, post, is_class_m, grade])
        conn.commit()
        logger.info('Регистрация пользователя {}, user_id:{}'.format(name, user_id))
    return status.status


@logger.catch
def change_user_name(user_id, new_name):
    with database() as (cur, conn, status):
        sql = "UPDATE users SET name = %s WHERE user_id = %s"
        cur.execute(sql, [new_name, user_id])
        conn.commit()
    return status.status


@logger.catch
def change_user_photo(user_id, new_photo):
    with database() as (cur, conn, status):
        sql = "UPDATE users SET photo_id = %s WHERE user_id = %s"
        cur.execute(sql, [new_photo, user_id])
        conn.commit()
    return status.status


@logger.catch
def change_user_direction(user_id, new_direction):
    with database() as (cur, conn, status):
        sql = "UPDATE users SET direction = %s WHERE user_id = %s"
        cur.execute(sql, [new_direction, user_id])
        conn.commit()
    return status.status


@logger.catch
def change_user_bio(user_id, new_bio):
    with database() as (cur, conn, status):
        sql = "UPDATE users SET bio = %s WHERE user_id = %s"
        cur.execute(sql, [new_bio, user_id])
        conn.commit()
    return status.status


@logger.catch()
def delete_user(user_id):
    with database() as (cur, conn, status):
        sql = "DELETE FROM users WHERE user_id = %s"
        cur.execute(sql, [user_id])
        conn.commit()
        logger.info('Удален пользователь {}'.format(user_id))
    return status.status


@logger.catch
def add_mentor(user_id, tg_nick, file_id, direction, bio):
    with database() as (cur, conn, status):
        sql = "UPDATE USERS SET tg_nick = %s, photo_id = %s, direction = %s, bio = %s, is_admin=1, is_confirmed=0" \
              " WHERE user_id = %s"
        cur.execute(sql, [tg_nick, file_id, direction, bio, user_id])
        conn.commit()
        logger.info('Регистрация заявки наставника user_id: {}'.format(user_id))
    return status.status


@logger.catch
def confirm_mentor(mentor_id):
    with database() as (cur, conn, status):
        sql = "UPDATE users SET is_confirmed=1 WHERE user_id = %s"
        cur.execute(sql, [mentor_id])
        conn.commit()
        logger.info("Подтверждение наставника {}".format(mentor_id))
    return status.status


@logger.catch
def add_question(message_id, from_user, question, topic):
    question_date = dt.date.today()
    with database() as (cur, conn, status):
        sql = "INSERT INTO question (message_id, from_user, question_text, question_date, topic, is_valid)" \
              " VALUES (%s, %s, %s, %s, 0) RETURNING question_id"
        cur.execute(sql, [message_id, from_user, question, question_date, topic])
        question_id = cur.fetchone()[0]
        conn.commit()
        logger.info("Задан вопрос по теме {}: {}".format(topic, question))
    return status.status, question_id


@logger.catch
def set_non_valid_question(questions_id):
    with database() as (cur, conn, status):
        sql = "UPDATE questions SET is_active = 0 WHERE id = ANY(%s)"
        cur.execute(sql, [questions_id])
    return status.status
            