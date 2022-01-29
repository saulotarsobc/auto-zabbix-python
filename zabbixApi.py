import requests
import json
from configparser import ConfigParser

config = ConfigParser()
config.read('./config.ini')

url = config.get('auth', 'url')
user = config.get('auth', 'user')
password = config.get('auth', 'password')


def login():
    try:
        r = requests.post(url, json={
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": user,
                "password": password},
            "id": 1
        })
        AUTHTOKEN = r.json()["result"]
        print(f"\n>>>>>>>>>> Login: {AUTHTOKEN}\n")
        return AUTHTOKEN
    except Exception:
        print(f"Nao consegui logar")


def logout(AUTHTOKEN):
    if (AUTHTOKEN):
        try:
            r = requests.post(url, json={"jsonrpc": "2.0", "method": "user.logout", "params": {
            }, "id": 2, "auth": AUTHTOKEN})
            print(f"\n>>>>>>>>>> Logout: {json.dumps(r.json()['result'])}")
        except Exception as err:
            print("logout: ", err)
