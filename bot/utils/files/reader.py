import os

import pandas as pd


def read_posts(dir_path):
    file_name = 'posts.xlsx'
    file_path = os.path.join(dir_path, file_name)
    return pd.read_excel(file_path)
 