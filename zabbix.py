from configparser import ConfigParser
import requests
import json

""" credenciais de acesso ao zabbix no arquivo 'config.ini'"""
"""
[auth]
url = http://<ip_do_zabbix>/zabbix/api_jsonrpc.php
user = <user_do_zabbix>
password = <senha_do_zabbix>
"""

config = ConfigParser()
config.read('./config.ini')
url = config.get('auth', 'url')
user = config.get('auth', 'user')
password = config.get('auth', 'password')


def login(tipo_de_login):
    if tipo_de_login == 1:
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
            print(f"\nLogado com Usuario e Senha\n")
            print(f"\n>>>>>>>>>> Login: {AUTHTOKEN}\n")
            return AUTHTOKEN
        except Exception:
            exit(f"Nao consegui logar")
    else:
        token = config.get('auth', 'token')
        print(f"\nLogado via API Token\n")
        print(f"\n>>>>>>>>>> Login: {token}\n")
        return token


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


def getTemplates(AUTHTOKEN):
    try:
        r = requests.post(url, json={
            "jsonrpc": "2.0",
            "method": "template.get",
            "params": {
                "output": "extend",
                "filter": {
                    "host": []
                }
            },
            "auth": AUTHTOKEN,
            "id": 1
        })
        res = r.json()
        return res
    except Exception:
        print(f"\nerror\n")


def criarHosts(AUTHTOKEN, nome, dns, tipo_interface, port_interface, templates, id_grupo):
    # print(AUTHTOKEN, nome, ip, snmp_c, tipo_interface, port_interface, templates, id_grupo)
    try:
        r = requests.post(url, json={
            "jsonrpc": "2.0",
            "method": "host.create",
            "params": {
                "host": nome,
                "interfaces": [
                    {
                        "type": tipo_interface,
                        "main": 1,
                        "useip": 0,
                        "ip": "",
                        "dns": dns,
                        "port": port_interface,
                    }
                ],
                "groups": [
                    {
                        "groupid": id_grupo
                    }
                ],
                "templates": templates,
            },
            "auth": AUTHTOKEN,
            "id": 5
        })
        res = r.json()
        if 'error' in res:
            print(
                f'Host {nome} => { json.dumps(r.json()["error"]["data"]) }')
        else:
            print(
                f'Host "{nome}" => Criado com o ID { json.dumps(r.json()["result"]["hostids"]) }')
    except Exception:
        print(f"\nerror\n")


def logout(AUTHTOKEN, tipo_de_login):
    if tipo_de_login == 1:
        try:
            r = requests.post(url, json={
                "jsonrpc": "2.0",
                "params": {},
                "method": "user.logout",
                "id": 100,
                "auth": AUTHTOKEN
            })
            print(f"\n>>>>>>>>>> Logout: {json.dumps(r.json()['result'])}\n")
            # print(f"Fim da aplicação\n")
        except Exception as err:
            print(f"\nlogout: ", err)
    # else:
        # print(f"\nFim da aplicação\n")
