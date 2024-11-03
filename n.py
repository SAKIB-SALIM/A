import os
from random import randrange
random_value = f"{randrange(100)}.{randrange(100)}.{randrange(100)}"

with open(os.environ['GITHUB_ENV'], 'a') as env_file:
    env_file.write(f'K={random_value}\n')
