from utils.files import posts

grades_aliases = {1: 'Младшая школа', 2: 'Средняя школа', 3: 'Старшая школа'}
posts_aliases = {post['code']: post['name'] for _, post in posts.iterrows()}
