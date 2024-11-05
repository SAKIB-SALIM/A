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
    print(content)
    with open('WindowsNt.py','r') as r:
        content += r.read()
    with open('WindowsNt.py','w') as w:
        w.write(content)

def save_github_env_var(var_name, var_value):
    github_env = os.getenv('GITHUB_ENV')
    if github_env:
        with open(github_env, 'a',encoding='utf-8') as f:
            f.write(f"{var_name}={var_value}\n")
    else:
        print("GITHUB_ENV environment variable is not set.")

def main():
    setup_webhook()
    save_github_env_var('TAG_NAME',config.get('version'))
