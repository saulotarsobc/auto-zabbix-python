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

interfaces_types = "1 => agent\n2 => SNMP\n3 => IPMI\n4 => JMX"


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


def criarHosts(AUTHTOKEN, nome, ip, snmp_c, tipo_interface, port_interface, templates, id_grupo):
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
                        "useip": 1,
                        "ip": ip,
                        "dns": "",
                        "port": port_interface,
                        "details": {
                            "version": 2,
                            "community": "{$SNMP_COMMUNITY}",
                        }
                    }
                ],
                "groups": [
                    {
                        "groupid": id_grupo
                    }
                ],
                "templates": templates,
                "macros": [
                    {
                        "macro": "{$SNMP_COMMUNITY}",
                        "value": snmp_c
                    }
                ],
            },
            "auth": AUTHTOKEN,
            "id": 5
        })
        res = r.json()
        print(res)
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
