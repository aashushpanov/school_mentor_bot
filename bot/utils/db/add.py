import pandas as pd
from psycopg2.extras import Json
import datetime as dt

from pandas import DataFrame, Series

from .connect import database


def add_user(user_id, name, post, is_class_m, grade):
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
        sql = "INSERT INTO users (user_id, name, post, is_class_m, grade, is_admin) VALUES (%s, %s, %s, %s, %s, 0)"
        curr.execute(sql, [user_id, name, post, is_class_m, grade])
        conn.commit()
    return status.status

