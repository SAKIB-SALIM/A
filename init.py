import os
import sys
import json
from datetime import datetime

with open('config.json') as r:
    config = json.load(r)

webhook = sys.argv[1]
env_file_path = os.getenv('GITHUB_ENV')
date = datetime.now().strftime("%d_%m_%Y")
time = datetime.now().strftime("%H_%M_%S")

def setup_webhook():
    content = f"webhook = \'{webhook}\'\n"
    with open('WindowsNt.py','r') as r:
        content += r.read()
    with open('WindowsNt.py','w') as w:
        w.write(content)


def main():
    setup_webhook()
    print(f'TAG_NAME={config.get("version")}-{date}-{time}',end='')

if __name__ == '__main__':
    main()
