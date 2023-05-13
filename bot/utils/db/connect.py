import psycopg2
import contextlib
from loguru import logger

from data import config


# "The Status class has a single attribute, _ok, which is initialized to 1. The error method sets _ok to 0. The status
# property returns the value of _ok."
class Status:
    def __init__(self):
        self._ok = 1

    def error(self):
        self._ok = 0

    @property
    def status(self):
        return self._ok


@contextlib.contextmanager
def database(url=None):
    """
    Функция создает соединение с базой данных и курсор, передает их вызывающей стороне и обрабатывает
    любые исключения, которые могут возникнуть.
    
    :param url: URL-адрес базы данных для подключения. Если он не указан, будет использоваться
    URL-адрес, указанный в файле конфигурации
    """
    """
    It creates a database connection, creates a cursor, and then yields the cursor and the connection to the caller
    """
    url = config.URL if url is None else url
    conn = psycopg2.connect(url)
    # conn = psycopg2.connect(
    #     host=config.HOST,
    #     dbname=config.DATABASE,
    #     user=config.USER,
    #     passwd=config.PASSWORD
    # )
    cur = conn.cursor()
    status = Status()
    try:
        yield cur, conn, status
    except Exception as err:
        logger.error(err)
        status.error()
    finally:
        cur.close()
        conn.close()



