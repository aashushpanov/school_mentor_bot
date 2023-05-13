import os

import pandas as pd


def read_posts(dir_path):
    file_name = 'posts.xlsx'
    file_path: str = os.path.join(dir_path, file_name)
    return pd.read_excel(file_path)


def read_topics(dir_path):
    file_name = 'topics.xlsx'
    file_path: str = os.path.join(dir_path, file_name)
    topics = pd.read_excel(file_path)
    not_found_topic = pd.DataFrame([['nf', 'Нет нужной категории']], columns=['code', 'name'])
    topics = pd.concat([topics, not_found_topic])
    file_name = 'questions.xlsx'
    file_path: str = os.path.join(dir_path, file_name)
    questions = pd.read_excel(file_path)
    for _, topic in topics.iterrows():
        not_found_question = pd.DataFrame([[topic['code'], 'nf', 'Задать свой вопрос', '']],
                                          columns=['topic', 'rang', 'question', 'answer'])
        questions = pd.concat([questions, not_found_question])
    return topics, questions


def read_topic_chats(dir_path):
    file_name = 'topic_chats.xlsx'
    file_path: str = os.path.join(dir_path, file_name)
    return pd.read_excel(file_path)
