# Zabbix + Python

> Automação de cadastros de hosts no Zabbix a partir de uma lista em CSV. Possibilidade de logar com Usuário e Senha ou via Token API.

---

## Video

### [Automatizando cadastros de Hosts no Zabbix com Python](https://youtu.be/ZmQtVOMZ7EQ)

---

## config.ini

> Nesse arquivo você configura as credenciais de acesso ao seu Zabbix.

```ini
[auth]
url = http://meu-server.com/zabbix/api_jsonrpc.php
user = Admin
password = SuperSenha
token = tOkEn_De_AcEsSo_123
```

---

## hosts.csv

```csv
nome,ip,tipo,{$SNMP_COMMUNITY},porta
Teste Via Api 01,10.10.10.1,2,21323fgserwt4t,161
Teste Via Api 02,10.10.10.2,2,21323fgserwt4t,161
Teste Via Api 03,10.10.10.3,2,21323fgserwt4t,162
Teste Via Api 04,10.10.10.4,2,21323fgserwt4t,161
```

---

## Python

> Altere a váriavel **'tipo_de_login'** para **1** caso queira logar via *Usuário* e *Senha* ou **2** para logar via *Token*.

```py
...

    """
    [tipo de login]
    1 = usuario e senha
    2 = api token
    """
    tipo_de_login = 2

...
```
