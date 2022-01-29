import readCsv
import zabbixApi

AUTHTOKEN = zabbixApi.login()

hosts = readCsv.getHosts('./hosts.csv')

for i in hosts:
    print(f"{i['nome']} => {i['ip']}")


zabbixApi.logout(AUTHTOKEN)
