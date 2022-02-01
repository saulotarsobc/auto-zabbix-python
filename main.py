#! /usr/bin/python
import readCsv
import zabbix

file_csv = 'hosts.csv'
criar_grupo = ""
grupos = ""
associar_template = ""
templates = []

# Logar no zabbix
AUTHTOKEN = zabbix.login()

# Ler arquivo csv
hosts = readCsv.getHosts(file_csv)

# Criar grupo ?
while criar_grupo == "":
    criar_grupo = (input('Criar novo grupo? S | N: ').upper())

# Criar grupo
if criar_grupo == 'S':
    while grupos == "":
        nome_grupo = (input('Qual o nome do novo grupo?: '))
        res = zabbix.criarGrupo(AUTHTOKEN, nome_grupo)
        if 'error' in res:
            print(f'\nErro: {res["error"]["data"]}\n')
        else:
            grupos = res['result']['groupids'][0]
            print(f'\nO grupo "{nome_grupo}" com ID "{grupos}" foi criado\n')

# Listar Grupos existentes
if criar_grupo == 'N':
    while grupos == "":
        grupos = zabbix.getGroups(AUTHTOKEN)
        for grupo in grupos['result']:
            print(f'{grupo["groupid"]} => {grupo["name"]}')
        grupos = input('\nInsira o ID do Grupo: ')
        print(f'\nGrupo: {grupos}\n')

# Associar a template existente?
while associar_template == "":
    associar_template = (
        input('\nAssociar a um template existente? S | N : ').upper())

# Se associar a um template, SIM
if associar_template == 'S':
    res = zabbix.getTemplates(AUTHTOKEN)
    for i in res['result']:
        print(f'{i["templateid"]} => {i["name"]}')
    while templates == []:
        x = str(input(
            '\nInsira o ID do Template. \nSe for escolher mais de um, separe por virgula: '))
        if ',' in x:
            xs = x.split(',')
            for i in xs:
                templates.append({'templateid': i})
        else:
            templates.append({'templateid': x})

    print('\n', templates)

# Se associar a um template, NAO
if associar_template == 'N':
    templates = []

# Criar hosts
for host in hosts:
    zabbix.criarHosts(
        AUTHTOKEN, host['nome'], host['ip'], host['{$SNMP_COMMUNITY}'], host['tipo'], host['porta'], templates, grupos)

# Deslogar
zabbix.logout(AUTHTOKEN)
