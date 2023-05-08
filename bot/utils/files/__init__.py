from os import path

from utils.files.reader import read_posts


dir_path = path.join('data', 'files')

posts = read_posts(dir_path)
