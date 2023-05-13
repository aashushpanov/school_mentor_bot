import pandas
import datetime as dt
import pytz
from utils.db.get import get_all_non_answered_q
from utils.db.add import set_non_valid_question


def now():
    return dt.datetime.now(pytz.timezone('Europe/Moscow')).date()


def update_question_validity():
    questions = get_all_non_answered_q()
    non_valid_questions = []
    for _, question in questions.iterrows():
        if now() - question['question_date'] == 2:
            non_valid_questions.append(question['id'])
    _ = set_non_valid_question(non_valid_questions)
