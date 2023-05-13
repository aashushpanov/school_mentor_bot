import os

from utils.files.reader import read_posts, read_topics, read_topic_chats

wd = os.getcwd()
dir_path = os.path.join(wd, 'bot', 'data', 'files')

posts = read_posts(dir_path)
topics, questions = read_topics(dir_path)
topic_chats = read_topic_chats(dir_path)
