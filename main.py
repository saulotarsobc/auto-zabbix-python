import readCsv
import zabbix

file_csv = 'hosts.csv'
criar_grupo = ""
id_grupo = ""


""" Logar no zabbix """
AUTHTOKEN = zabbix.login()


""" Ler arquivo csv """
hosts = readCsv.getHosts(f"./{file_csv}")


""" Criar grupo ? """
while criar_grupo == "":
    criar_grupo = (input('Criar novo grupo? S | N : ').upper())


""" Criar grupo """
if criar_grupo == 'S':
    while id_grupo == "":
        nome_grupo = (input('Qual o nome do novo grupo?: '))
        res = zabbix.criarGrupo(AUTHTOKEN, nome_grupo)
        if 'error' in res:
            print(f'\nErro: {res["error"]["data"]}\n')
        else:
            id_grupo = res['result']['groupids'][0]
            print(f'\nO grupo "{nome_grupo}" com ID "{id_grupo}" foi criado\n')

""" Listar Grupos existentes """
if criar_grupo == 'N':
    while id_grupo == "":
        grupos = zabbix.getGroups(AUTHTOKEN)
        for grupo in grupos['result']:
            print(f'{grupo["groupid"]} => {grupo["name"]}')
        id_grupo = input('\nInsira o ID do Grupo: ')
        print(f'\nGrupo: {id_grupo}\n')

print(hosts)

""" Deslogar """
zabbix.logout(AUTHTOKEN)
