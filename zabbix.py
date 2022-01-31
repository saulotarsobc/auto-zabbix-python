from configparser import ConfigParser
import requests
import json

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


def criarGrupo(AUTHTOKEN, nome_grupo):
    try:
        r = requests.post(url, json={
            "jsonrpc": "2.0",
            "method": "hostgroup.create",
            "params": {
                "name": nome_grupo
            },
            "auth": AUTHTOKEN,
            "id": 2
        })
        res = r.json()
        return res
    except Exception:
        print(f"\nerror\n")


def getGroups(AUTHTOKEN):
    try:
        r = requests.post(url, json={
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output": "extend",
                "status": 0
            },
            "auth": AUTHTOKEN,
            "id": 1
        })
        res = r.json()
        return res
    except Exception:
        print(f"\nerror\n")


def logout(AUTHTOKEN):
    if (AUTHTOKEN):
        try:
            r = requests.post(url, json={"jsonrpc": "2.0", "method": "user.logout", "params": {
            }, "id": 100, "auth": AUTHTOKEN})
            print(f"\n>>>>>>>>>> Logout: {json.dumps(r.json()['result'])}")
        except Exception as err:
            print("logout: ", err)
